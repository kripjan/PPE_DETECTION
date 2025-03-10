import datetime
import cv2
from flask import current_app
from app import db
from app.models.object import Object
from app.models.detection_object import DetectionObject
from app.models.detection import Detection
from ultralytics import YOLO
from flask_socketio import emit
from flask import request
from flask_mail import Message
from flask_login import current_user
from app import mail

# Load YOLO model
model = YOLO("app/models/first.pt")


# Global variable to track the last saved detection time
last_saved_time = None


def send_ppe_violation_email(violation_details):
    if current_user.is_authenticated:  # Ensure user is logged in
        to_email = current_user.email  # Get the logged-in user's email
        subject = "PPE Violation Alert!"
        body = f"Hello {current_user.username},\n\nA PPE violation was detected:\n\n{violation_details}"

        msg = Message(subject, recipients=[to_email], body=body)
        mail.send(msg)


def save_violating_detection(frame, results, company_id):
    """Save detection data to the database if violations are detected."""
    global last_saved_time
    current_time = datetime.datetime.now()

    # Ensure 5 minutes have passed since the last detection save
    if (
        last_saved_time is None
        or (current_time - last_saved_time).total_seconds() >= 300
    ):
        violations_detected = False
        detected_objects = set()
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cls_idx = int(box.cls[0])
                label = result.names.get(cls_idx, "Unknown")

                if label in {"NO-Hardhat", "NO-Safety Vest", "NO-Mask"}:
                    # Mark the presence of a safety violation
                    violations_detected = True
                    detected_objects.add(label)

        if violations_detected:
            try:
                # Convert frame to binary data
                _, buffer = cv2.imencode(".jpg", frame)
                frame_bytes = buffer.tobytes()

                # Save detection to the database
                new_detection = Detection(
                    datetime=current_time, image_data=frame_bytes, company_id=company_id
                )
                db.session.add(new_detection)
                db.session.flush()  # Obtain the detection ID

                # Save related detected objects
                for obj_name in detected_objects:
                    obj = Object.query.filter_by(name=obj_name).first()
                    if obj:
                        detection_object = DetectionObject(
                            detection_id=new_detection.id, object_id=obj.id
                        )
                        db.session.add(detection_object)

                # Commit changes
                db.session.commit()
                last_saved_time = current_time

            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Error saving detection to database: {e}")


def generate_livefeed(company_id):
    """Open webcam, process frames, and stream to the client."""
    cam = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                break

            # Perform inference
            results = model(frame)

            # Draw bounding boxes on the frame
            person_count = 0  # Counter for persons in frame

            for result in results:
                safety_items = {
                    "Hardhat": [],
                    "Safety Vest": [],
                    "NO-Hardhat": [],
                    "NO-Safety Vest": [],
                    "Person": [],
                }

                # Categorize detections
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    cls_idx = int(box.cls[0])
                    label = result.names.get(cls_idx, "Unknown")

                    if label in safety_items:
                        safety_items[label].append((x1, y1, x2, y2))

                # Count number of persons in the frame
                person_count = len(safety_items["Person"])

                # Draw bounding boxes
                for label, items in safety_items.items():
                    for x1, y1, x2, y2 in items:
                        if label in ["Hardhat", "Safety Vest"]:
                            color = (0, 255, 0)  # Green
                        elif label in ["NO-Hardhat", "NO-Safety Vest"]:
                            color = (0, 0, 255)  # Red
                        elif label == "Person":
                            color = (255, 0, 0)  # Blue
                        else:
                            continue  # Skip bounding box for other labels

                        # Draw the bounding box and label
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        cv2.putText(
                            frame,
                            label,
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,
                            color,
                            2,
                        )

            # Display the person count in the top-left corner
            cv2.putText(
                frame,
                f"Persons: {person_count}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 0),  # White text color
                2,
                cv2.LINE_AA,
            )
            # Save frames with violations to the database
            save_violating_detection(frame, results, company_id)

            # Convert processed frame to JPEG for streaming
            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"

    finally:
        cam.release()
