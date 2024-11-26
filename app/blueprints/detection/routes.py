import datetime
import time
import cv2
from flask import Response, current_app, render_template, stream_with_context
from flask_login import login_required
from ultralytics import YOLO
from app import db
from app.blueprints.detection import detection
from app.models.frame_model import Frame
from app.models.object_model import Object
from app.models.frame_object_model import FrameObject
from PIL import Image
import io


# Load YOLO model
model = YOLO("app/models/best.pt")

# Global variable to track last saved frame time
last_saved_time = None

@detection.route('/livefeed', methods=['GET'])
@login_required
def live_feed_page():
    """
    Render the live feed page.
    """
    return render_template('live_feed_page.html')

@detection.route('/stream_livefeed', methods=['GET'])
@login_required
def stream_livefeed():
    """
    Stream the processed live video feed to the client.
    """
    with current_app.app_context():
        return Response(stream_with_context(generate_livefeed()), mimetype='multipart/x-mixed-replace; boundary=frame')

def generate_livefeed():
    """
    Open webcam, process frames through the YOLO model, and stream to the client.
    """
    cam = cv2.VideoCapture(0)
    try:
        while True:
            ret, frame = cam.read()
            if not ret:
                break

            # Perform inference
            results = model(frame)

            # Process frame
            processed_frame, detected_objects, violations_detected = process_frame(frame, results)

            # Save frames with violations to the database

            # Convert processed frame to JPEG for streaming
            _, buffer = cv2.imencode('.jpg', processed_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            if violations_detected:
                # with current_app.app_context():
                store_violating_frame(processed_frame, detected_objects, frame_bytes)
    finally:
        cam.release()

def process_frame(frame, results):
    """
    Process the frame: draw bounding boxes and extract relevant detection information.

    Args:
        frame: The current video frame.
        results: YOLO detection results.

    Returns:
        processed_frame: The frame with bounding boxes and labels drawn.
        detected_objects: Set of detected object labels.
        violations_detected: Boolean indicating if safety violations exist in the frame.
    """
    person_box = None
    no_safety_labels = {"NO-Hardhat", "NO-Safety Vest", "NO-Mask"}
    detected_objects = set()
    violations_detected = False

    for result in results:
        for box in result.boxes:
            # Extract bounding box coordinates and details
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            conf = box.conf[0]  # Confidence score
            cls_idx = int(box.cls[0])
            label = result.names.get(cls_idx, "Unknown")

            # Assign color and check for violations
            if label == "Person":
                color = (255, 0, 0)  # Blue
                person_box = (x1, y1, x2, y2)
            elif label in no_safety_labels:
                color = (0, 0, 255)  # Red
                detected_objects.add(label)
            else:
                color = (0, 255, 0)  # Green

            # Draw bounding box and label
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)  # Draw label


            # Check for violations
            if label in no_safety_labels and person_box:
                px1, py1, px2, py2 = person_box
                if px1 <= x1 and py1 <= y1 and px2 >= x2 and py2 >= y2:
                    violations_detected = True

    return frame, detected_objects, violations_detected

def store_violating_frame(frame, detected_objects, frame_bytes):
    """
    Save the frame and detected objects to the database.
    
    This function assumes that violations have already been detected
    before being called, so no need to check for violations again here.
    """
    global last_saved_time
    current_time = datetime.datetime.now()

    # Check if 5 minutes have passed since the last saved frame
    if last_saved_time is None or (current_time - last_saved_time).total_seconds() >= 300:
        try:
            # with current_app.app_context():
            # Save frame metadata
            new_frame = Frame(datetime=current_time, camera_id=0, image_data=frame_bytes)  # Assuming camera ID is 0
            db.session.add(new_frame)
            db.session.flush()  # Get frame ID before committing

            # Save associated objects
            for obj_name in detected_objects:
                # with current_app.app_context():
                obj = Object.query.filter_by(object_name=obj_name).first()
                if obj:
                    new_frame_object = FrameObject(frame_id=new_frame.frame_id, object_id=obj.object_id)
                    db.session.add(new_frame_object)

            # with current_app.app_context():
            # Commit both frame and objects
            db.session.commit()
            last_saved_time = current_time

        except Exception as e:
            # with current_app.app_context():
            db.session.rollback()  # Rollback transaction if any error occurs
            current_app.logger.error(f"Error saving frame to database: {e}")

@detection.route('/reports', methods=['GET'])
def reports_page():
    return render_template('reports_page.html')

@detection.route('/frame_image/<int:frame_id>', methods=['GET'])
def get_frame_image(frame_id):
    """
    Retrieve and return the image stored in the database for the given frame ID.
    """
    frame = Frame.query.get(frame_id)
    if frame:
        return Response(frame.image_data, mimetype='image/jpeg')
    return 'Frame not found', 404


# Convert image to binary data
# image = Image.open("path_to_image.jpg")
# buffer = io.BytesIO()
# image.save(buffer, format="JPEG")
# image_data = buffer.getvalue()
