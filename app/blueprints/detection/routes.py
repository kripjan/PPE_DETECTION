from flask import Response, render_template, stream_with_context
from flask_login import login_required, current_user
from app import socketio
from app.blueprints.detection import detection
from app.blueprints.detection.services import *

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
    """Render the reports page."""
    return render_template("reports_page.html")
