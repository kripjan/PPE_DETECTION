from flask import Response, render_template, stream_with_context
from flask_login import login_required, current_user
from app import socketio
from app.blueprints.detection import detection
from app.blueprints.detection.services import *
import base64
from sqlalchemy.sql import func


detected_classes = set()


@detection.route("/livefeed", methods=["GET"])
@login_required
def live_feed_page():
    """Render the live feed page."""
    return render_template("live_feed_page.html")


@detection.route("/stream_livefeed", methods=["GET"])
@login_required
def stream_livefeed():
    """
    Stream the processed live video feed to the client.
    The live feed performs inference using the YOLO model and checks for violations every 5 minutes.
    If a violation is detected, it saves the detection to the database.
    """
    company_id = current_user.id  # Get the logged-in company's ID
    return Response(
        stream_with_context(generate_livefeed(company_id)),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


@socketio.on("connect")
def handle_connect():
    socketio.emit(
        "detection_update", {"detected_classes": detected_classes}, broadcast=True
    )


@detection.route("/reports")
@login_required
def reports_page():
    records = (
        db.session.query(
            Detection.id,
            Detection.datetime,
            Detection.image_data,
            func.string_agg(Object.name, ", ").label("object_names"),
        )
        .join(DetectionObject, Detection.id == DetectionObject.detection_id)
        .join(Object, DetectionObject.object_id == Object.id)
        .group_by(Detection.id, Detection.datetime, Detection.image_data)
        .all()
    )

    processed_records = []
    for record in records:
        try:
            image_base64 = None
            if record.image_data:  # Ensure image_data is not None
                if isinstance(record.image_data, memoryview):
                    record.image_data = (
                        record.image_data.tobytes()
                    )  # Convert memoryview to bytes

                image_base64 = base64.b64encode(record.image_data).decode("utf-8")

            processed_records.append(
                {
                    "id": record.id,
                    "datetime": record.datetime,
                    "image_data": image_base64,
                    "object_names": record.object_names,  # Object name from the `object` table
                }
            )
        except Exception as e:
            print(f"Error processing record {record.id}: {e}")

    return render_template("reports_page.html", records=processed_records)
