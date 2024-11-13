from database import db

# Objects Model
class Object(db.Model):
    __tablename__ = 'objects'

    object_id = db.Column(db.Integer, primary_key=True)
    object_name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Object {self.object_name}>"