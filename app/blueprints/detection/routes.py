import datetime
import time
import cv2
from flask import Response, current_app, render_template
from flask_login import login_required
from ultralytics import YOLO
from app import db
from app.blueprints.detection import detection
from app.models.frame_model import Frame
from app.models.object_model import Object
from app.models.frame_object_model import FrameObject

# Load the YOLO model
model = YOLO("app/models/best.pt")

# Variables to track time for 5-minute intervals
last_saved_time = None

@detection.route('/stream_livefeed')
@login_required
def stream_livefeed():
    # Stream the frames from the `generate_livefeed` function
    return Response(generate_livefeed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@detection.route('/livefeed', methods=['GET'])
@login_required
def live_feed_page():
    # Render the HTML page with the video feed placeholder
    return render_template('live_feed_page.html')

def save_frame_and_objects(frame, frame_datetime, camera_id, detected_objects):
    """
    Save the frame and associated detected objects to the database.

    Args:
        frame: The frame to save (unused in this case, could be extended for actual image saving).
        frame_datetime: The datetime when the frame was captured.
        camera_id: The camera ID associated with the frame.
        detected_objects: List of object labels detected in the frame.
    """
    # Save the frame metadata
    new_frame = Frame(datetime=frame_datetime, camera_id=camera_id)
    db.session.add(new_frame)
    db.session.commit()

    # Save the detected objects associated with the frame
    for obj_name in detected_objects:
        obj = Object.query.filter_by(objectname=obj_name).first()
        if obj:
            new_frame_object = FrameObject(frameid=new_frame.frame_id, objectid=obj.object_id)
            db.session.add(new_frame_object)
    db.session.commit()

def process_and_save_frame(frame, results, frame_datetime, camera_id):
    """
    Process the detection results, check conditions, and save the frame if required.

    Args:
        frame: The current video frame.
        results: YOLO detection results.
        frame_datetime: The datetime when the frame was captured.
        camera_id: The camera ID associated with the frame.
    """
    global last_saved_time

    # Initialize variables to check bounding box conditions
    person_box = None
    no_safety_labels = {"NO-Hardhat", "NO-Safety Vest", "NO-Mask"}
    detected_objects = set()
    safety_violations_detected = False

    for result in results:
        for box in result.boxes:
            # Extract bounding box coordinates, confidence, and class index
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cls_idx = int(box.cls[0])
            label = result.names.get(cls_idx, "Unknown")

            # Determine the color for the bounding box
            if label == "Person":
                color = (255, 0, 0)  # Blue for Person
                person_box = (x1, y1, x2, y2)
            elif label in no_safety_labels:
                color = (0, 0, 255)  # Red for NO- labels
                detected_objects.add(label)
            else:
                color = (0, 255, 0)  # Green for other objects

            # Draw the bounding box and label on the frame
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, f'{label}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Check if safety violation objects are inside the person bounding box
            if label in no_safety_labels and person_box:
                px1, py1, px2, py2 = person_box
                if px1 <= x1 and py1 <= y1 and px2 >= x2 and py2 >= y2:
                    safety_violations_detected = True

    # Save the frame if conditions are met
    if person_box and safety_violations_detected:
        # Save every 5 minutes
        if last_saved_time is None or (time.time() - last_saved_time >= 300):
            save_frame_and_objects(frame, frame_datetime, camera_id, detected_objects)
            last_saved_time = time.time()


def generate_livefeed():
    """
    Capture frames from the webcam, process them, and stream to the client.
    """
    cam = cv2.VideoCapture(0)
    camera_id = 0  # Set the appropriate camera ID

    # Capture the app context before starting the generator
    app_context = current_app._get_current_object()

    while True:
        ret, frame = cam.read()  # Capture frame from webcam
        if not ret:
            break  # Break the loop if there's an issue with the frame

        # Perform inference
        results = model(frame)

        # Get the current datetime
        frame_datetime = datetime.datetime.now()

        # Process and save frames based on the detection results
        with app_context.app_context():
            process_and_save_frame(frame, results, frame_datetime, camera_id)

        # Convert the frame to JPEG format for streaming
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                conf = box.conf[0]
                cls_idx = int(box.cls[0])
                label = result.names.get(cls_idx, "Unknown")
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cam.release()  # Release the webcam

@detection.route('/reports', methods=['GET'])
def reports_page():
    return render_template('reports_page.html')
