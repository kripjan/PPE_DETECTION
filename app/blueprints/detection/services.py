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
            # Group detections by class
            persons, helmets, vests = [], [], []
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cls_idx = int(box.cls[0])
                label = result.names.get(cls_idx, "Unknown")

                if label == "Person":
                    persons.append((x1, y1, x2, y2))
                elif label == "Helmet":
                    helmets.append((x1, y1, x2, y2))
                elif label == "Vest":
                    vests.append((x1, y1, x2, y2))

            # Check for violations for each person
            for person in persons:
                px1, py1, px2, py2 = person
                has_helmet, has_vest = False, False

                # Check if helmets or vests overlap with the person bounding box
                for hx1, hy1, hx2, hy2 in helmets:
                    if hx1 >= px1 and hy1 >= py1 and hx2 <= px2 and hy2 <= py2:
                        has_helmet = True
                        break

                for vx1, vy1, vx2, vy2 in vests:
                    if vx1 >= px1 and vy1 >= py1 and vx2 <= px2 and vy2 <= py2:
                        has_vest = True
                        break

                # Record violation if the person lacks both helmet and vest
                if not (has_helmet and has_vest):
                    violations_detected = True
                    detected_objects.update(["Person", "Helmet", "Vest"])

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

            # Save frames with violations to the database
            save_violating_detection(frame, results, company_id)

            # Draw bounding boxes on the frame
            for result in results:
                safety_items = {
                    "Hardhat": [],
                    "Safety Vest": [],
                    "NO-Hardhat": [],
                    "NO-Safety Vest": [],
                    "Mask": [],
                    "NO-Mask": [],
                    "Person": [],
                }

                # Categorize detections
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    cls_idx = int(box.cls[0])
                    label = result.names.get(cls_idx, "Unknown")

                    if label in safety_items:
                        safety_items[label].append((x1, y1, x2, y2))

                # Draw bounding boxes
                for label, items in safety_items.items():
                    for x1, y1, x2, y2 in items:
                        if label in ["Hardhat", "Safety Vest", "Mask"]:
                            color = (0, 255, 0)  # Green
                        elif label in ["NO-Hardhat", "NO-Safety Vest", "NO-Mask"]:
                            color = (0, 0, 255)  # Red
                        elif label in ["Person"]:
                            color = (255, 0, 0)
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
            # # Send detected classes to the frontend
            # if detected_classes:
            #     send_detection_update(list(detected_classes))

            # Convert processed frame to JPEG for streaming
            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"

    finally:
        cam.release()
