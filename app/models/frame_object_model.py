from database import db

# FrameObject Model (Bridge Table between Frames and Objects)
class FrameObject(db.Model):
    __tablename__ = 'frame_object'

    frame_id = db.Column(db.Integer, db.ForeignKey('frames.frame_id'), primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('objects.object_id'), primary_key=True)

    frame = db.relationship('Frame', backref='frame_objects')
    object = db.relationship('Object', backref='frame_objects')

    def __repr__(self):
        return f"<FrameObject frame_id={self.frame_id}, object_id={self.object_id}>"