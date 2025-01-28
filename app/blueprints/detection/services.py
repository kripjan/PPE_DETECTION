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

            # Extract all detections
            persons = []
            helmets = []
            vests = []

            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                cls_idx = int(box.cls[0])
                label = result.names.get(cls_idx, "Unknown")

                # Group detections by class
                if label == "Person":
                    persons.append((x1, y1, x2, y2))
                elif label == "Helmet":
                    helmets.append((x1, y1, x2, y2))
                elif label == "Vest":
                    vests.append((x1, y1, x2, y2))

            # Check for violations
            for person in persons:
                px1, py1, px2, py2 = person
                person_has_helmet = False
                person_has_vest = False

                # Check if any helmet is inside the person bounding box
                for helmet in helmets:
                    hx1, hy1, hx2, hy2 = helmet
                    if hx1 >= px1 and hy1 >= py1 and hx2 <= px2 and hy2 <= py2:
                        person_has_helmet = True
                        break

                # Check if any vest is inside the person bounding box
                for vest in vests:
                    vx1, vy1, vx2, vy2 = vest
                    if vx1 >= px1 and vy1 >= py1 and vx2 <= px2 and vy2 <= py2:
                        person_has_vest = True
                        break

                # If the person does not have both helmet and vest, mark as violation
                if not (person_has_helmet and person_has_vest):
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
                person_detected = []
                equipment_detected = []
                head_detected = []  # Assuming head is a class in your dataset

                # Separate detections into person and equipment
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    cls_idx = int(box.cls[0])
                    label = result.names.get(cls_idx, "Unknown")
                    confidence = box.conf[0]

                    if label == "head":
                        head_detected.append((x1, y1, x2, y2))
                    elif label in ["helmet", "vest"]:
                        equipment_detected.append((x1, y1, x2, y2, label))

                # Draw bounding boxes for equipment
                for x1, y1, x2, y2, label in equipment_detected:
                    color = (0, 255, 0)  # Green for helmet and vest
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

                # Draw bounding boxes for persons (head without equipment)
                for px1, py1, px2, py2 in head_detected:
                    # Check if any equipment overlaps the head bounding box
                    has_equipment = False
                    for ex1, ey1, ex2, ey2, _ in equipment_detected:
                        # Simple overlap check
                        if ex1 < px2 and ex2 > px1 and ey1 < py2 and ey2 > py1:
                            has_equipment = True
                            break

                    if has_equipment:
                        color = (255, 0, 0)  # Blue for person with equipment
                    else:
                        color = (0, 0, 255)  # Red for person without equipment

                    cv2.rectangle(frame, (px1, py1), (px2, py2), color, 2)
                    cv2.putText(
                        frame,
                        "Person",
                        (px1, py1 - 10),
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
