from app import db


# DetectionObject Model (Bridge Table between Detection and Object)
class DetectionObject(db.Model):
    __tablename__ = "detection_object"

    detection_id = db.Column(
        db.Integer, db.ForeignKey("detection.id"), primary_key=True
    )
    object_id = db.Column(db.Integer, db.ForeignKey("object.id"), primary_key=True)

    detection = db.relationship("Detection", backref="objects")
    object = db.relationship("Object", backref="detections")

    def __repr__(self):
        return f"<DetectionObject detection_id={self.detection_id}, object_id={self.object_id}>"
