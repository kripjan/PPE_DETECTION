# In your auth blueprint or where your login route is
import math
import cv2
import cvzone
from flask import Response, render_template
# from .forms import LoginForm
from .. import monitoring_bp
from ultralytics import YOLO

# Load the YOLO model
model = YOLO("app\monitoring_bp_folder\models\ppe-detection-model.pt")

@monitoring_bp.route('/camerafeed', methods=['GET'])
def show_camerafeed():
    # Render the HTML page with the video feed placeholder
    return render_template('camerafeed_page.html')

def generate_feed():
    # Open the webcam
    cam = cv2.VideoCapture(0)

    while True:
        ret, frame = cam.read()  # Capture frame from webcam
        if not ret:
            break  # Break the loop if there's an issue with the frame

        # Perform inference
        results = model(frame)  # Use the model to perform detection

        # Process results
        for result in results:
            if len(result.boxes) > 0:  # Check if there are any detected boxes
                for box in result.boxes:  # Iterate through each box
                    # Extract bounding box coordinates, confidence, and class index
                    x1, y1, x2, y2 = box.xyxy[0].int().tolist()  # Get bounding box coordinates as integers
                    conf = box.conf[0]  # Confidence score
                    cls_idx = int(box.cls[0])  # Class index

                    # Ensure coordinates are integers
                    x1, y1, x2, y2 = map(int, (x1, y1, x2, y2))

                    # Get the label from the names dictionary
                    label = result.names[cls_idx] if cls_idx in result.names else "Unknown"

                    # Draw bounding box and label on the frame
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Draw bounding box
                    cv2.putText(frame, f'{label} {conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)  # Draw label

        # Convert the frame to JPEG format
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame for streaming
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cam.release()  # Release the webcam



@monitoring_bp.route('/video_feed')
def video_feed():
    # Stream the frames from the `generate_frames` function
    return Response(generate_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')
