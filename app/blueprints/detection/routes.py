import datetime
import time
import cv2
from flask import Response, render_template
from flask_login import login_required
from ultralytics import YOLO
from app import db
from app.blueprints.detection import detection
from app.models.frame_model import Frame
from app.models.object_model import Object
from app.models.frame_object_model import FrameObject

# Load the YOLO model
model = YOLO("app/models/ppe-detection-model.pt")

# Variable to track last frame datetime for 5-minute intervals
last_frame_datetime = None
detection_started = False

@detection.route('/stream_livefeed')
# @login_required
def stream_livefeed():
    # Stream the frames from the `generate_feed` function
    return Response(generate_livefeed(), mimetype='multipart/x-mixed-replace; boundary=frame')

@detection.route('/livefeed', methods=['GET'])
@login_required
def live_feed_page():
    # Render the HTML page with the video feed placeholder
    return render_template('live_feed_page.html')

def save_frame_to_db(frame_datetime, camera_id, frame_objects):
    new_frame = Frame(datetime=frame_datetime, camera_id=camera_id)
    db.session.add(new_frame)
    db.session.commit()

    for obj_name in frame_objects:
        obj = Object.query.filter_by(objectname=obj_name).first()
        if obj:
            new_frame_object = FrameObject(frameid=new_frame.frame_id, objectid=obj.object_id)
            db.session.add(new_frame_object)
    db.session.commit()

def generate_livefeed():
    global last_frame_datetime, detection_started

    # Open the webcam
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()  # Capture frame from webcam
        if not ret:
            break  # Break the loop if there's an issue with the frame

        # Perform inference
        results = model(frame)  # Use the model to perform detection

        objects_detected = any(len(result.boxes) > 0 for result in results)

        if objects_detected and not detection_started:
            # Start the detection process
            detection_started = True
            last_record_time = time.time()  # Reset the time when detection starts

        if detection_started:
            current_time = time.time()
            frame_datetime = datetime.datetime.now()
            camera_id = 2  # id of webcam in the database

            # Record frames every 5 minutes (300 seconds) after detection starts
            if last_frame_datetime is None or (frame_datetime - last_frame_datetime).total_seconds() >= 300:
                last_frame_datetime = frame_datetime

                # List of objects to detect in the frame
                required_objects = ["Person", "NO-Hardhat", "NO-Safety Vest"]
                frame_objects = []

                # Process results to detect relevant objects
                for result in results:
                    if len(result.boxes) > 0:
                        for box in result.boxes:
                            x1, y1, x2, y2 = box.xyxy[0].int().tolist()  # Get bounding box coordinates
                            conf = box.conf[0]
                            cls_idx = int(box.cls[0])

                            label = result.names[cls_idx] if cls_idx in result.names else "Unknown"

                            # If detected object is relevant, add it to the list
                            if label in required_objects:
                                frame_objects.append(label)

                # If a frame contains a "person" and either "no hardhat" or "no safety vest", save it
                if "Person" in frame_objects and any(obj in frame_objects for obj in ["NO-Hardhat", "NO-Safety Vest"]):
                    # Save this frame and link the detected objects directly here
                    save_frame_to_db(frame_datetime, camera_id, frame_objects)

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cam.release()  # Release the webcam

# In your auth blueprint or where your report route is
from flask import render_template, redirect, url_for, flash
from flask_login import login_required
from app.blueprints.detection import detection


@detection.route('/reports', methods=['GET'])
@login_required
def reports_page():
    return render_template('reports_page.html')


