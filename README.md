PPE Detection System
A web-based Personal Protective Equipment (PPE) detection system built for workplace safety compliance. The system uses a YOLOv8 deep learning model to monitor live webcam feeds in real-time, automatically detecting safety violations such as missing hardhats and safety vests, and alerting registered companies via email.
Features

Real-time Detection — Streams live webcam feed with bounding box overlays, classifying workers as compliant or non-compliant
Automated Alerts — Sends email notifications to the registered company when a PPE violation is detected
Violation Reports — Stores violation snapshots with timestamps in a PostgreSQL database and displays them in a searchable report table
Company Authentication — Companies register and log in to access their own detection data; sessions are protected with Flask-Login
WebSocket Support — Uses Flask-SocketIO for real-time detection updates on the frontend

Tech Stack Layers
Backend=Python, Flask, Flask-Login, Flask-Mail, Flask-SocketIOAI/MLYOLOv8 (Ultralytics), OpenCV, PyTorch (CUDA)
Database= PostgreSQL, SQLAlchemy
Frontend= HTML, CSS, Jinja2, JavaScript
Deployment = Docker, Docker Compose

How It Works

A company registers and logs in to the system
The live feed page opens the webcam and streams frames through the YOLO model
Each frame is analyzed for the presence of hardhats and safety vests
If a violation is detected, the frame is saved to the database with a timestamp (throttled to once every 5 minutes)
An email alert is sent to the company's registered address
All violations are viewable in the Reports page with images and detected object labels

Getting Started

git clone https://github.com/kripjan/PPE_DETECTION.git
cd PPE_DETECTION
docker-compose up --build
