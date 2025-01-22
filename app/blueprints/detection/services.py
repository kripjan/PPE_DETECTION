import datetime
import cv2
from flask import current_app
from app import db
from app.models.object import Object
from app.models.detection_object import DetectionObject
from app.models.detection import Detection
from ultralytics import YOLO

# YOLO model for detection
model = YOLO("app/models/best.pt")

# Global variable to track the last saved frame time
last_saved_time = None


def save_violating_detection(frame, results, company_id):
    """Save detection data to the database if violations are detected."""
    global last_saved_time
    current_time = datetime.datetime.now()

    # Check if 5 minutes have passed since the last saved detection
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
                db.session.flush()  # Get the detection ID

                # Save associated objects
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
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    cls_idx = int(box.cls[0])
                    label = result.names.get(cls_idx, "Unknown")
                    confidence = box.conf[0]

                    # Draw rectangle and label
                    if label == "Person":
                        color = (255, 0, 0)  # Blue for "Person"
                    elif "NO" in label:
                        color = (0, 0, 255)  # Red for violations (e.g., NO-Hardhat)
                    else:
                         color = (0, 255, 0)  # Green for other objects
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(
                        frame,
                        f"{label} {confidence:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        color,
                        2,
                    )

            # Convert processed frame to JPEG for streaming
            _, buffer = cv2.imencode(".jpg", frame)
            frame_bytes = buffer.tobytes()
            yield b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n"
    finally:
        cam.release()
