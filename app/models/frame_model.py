from app import db
from sqlalchemy import LargeBinary
from app.models.camera_model import Camera

# Frames Model
class Frame(db.Model):
    __tablename__ = 'frames'

    frame_id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.TIMESTAMP, nullable=False)
    camera_id = db.Column(db.Integer, db.ForeignKey('cameras.camera_id'), nullable=False)
    image_data = db.Column(LargeBinary, nullable=False)  # Column to store the image

    camera = db.relationship('Camera', backref='frames')

    def __repr__(self):
        return f"<Frame {self.frame_id} from Camera {self.camera_id}>"
