from ultralytics import YOLO
import cv2
import cvzone
import math

# Load the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Load the YOLO model
model = YOLO("ppe-detection-model.pt")

# Class names and color mapping
classNames = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone',
              'Safety Vest', 'machinery', 'vehicle']

# Store detected objects and their 'lifetime'
detected_objects = {}  # Store objects' positions and their frame counts

# Define the number of frames to persist the detection
PERSISTENCE_TIME = 30  # Keep annotations visible for 30 frames after detection

frame_count = 0

while True:
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture frame from webcam.")
        break

    # Perform inference only on every 5th frame for performance
    if frame_count % 5 == 0:
        results = model(img, stream=True)
        for r in results:
            boxes = r.boxes
            for box in boxes:
                # Bounding Box
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Confidence
                conf = math.ceil((box.conf[0] * 100)) / 100

                # Class Name
                cls = int(box.cls[0])
                if cls < len(classNames):
                    currentClass = classNames[cls]

                    # Store the detected object with position and persistence time
                    if conf > 0.5:
                        detected_objects[frame_count] = {
                            'class': currentClass,
                            'bbox': (x1, y1, x2, y2),
                            'conf': conf,
                            'countdown': PERSISTENCE_TIME
                        }

    # Decrease the countdown for each stored detection and remove expired ones
    expired_keys = []
    for key, value in detected_objects.items():
        if value['countdown'] > 0:
            # Draw the persistent annotation
            x1, y1, x2, y2 = value['bbox']
            currentClass = value['class']
            conf = value['conf']

            if currentClass in ['NO-Hardhat', 'NO-Safety Vest', 'NO-Mask']:
                myColor = (0, 0, 255)
            elif currentClass in ['Hardhat', 'Safety Vest', 'Mask']:
                myColor = (0, 255, 0)
            else:
                myColor = (255, 0, 0)

            cvzone.putTextRect(img, f'{currentClass} {conf}',
                               (max(0, x1), max(35, y1)), scale=1, thickness=1, colorB=myColor,
                               colorT=(255, 255, 255), colorR=myColor, offset=5)
            cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)

            # Decrease the countdown
            value['countdown'] -= 1
        else:
            expired_keys.append(key)

    # Remove expired annotations
    for key in expired_keys:
        del detected_objects[key]

    # Display the webcam feed
    cv2.imshow("Webcam Output", img)

    # Press 'q' to quit the webcam feed
    if cv2.waitKey(10) & 0xFF == ord('q'):
        print("Quitting and releasing resources...")
        break

    frame_count += 1

# Release everything when done
cap.release()
cv2.destroyWindow("Webcam Output")
