from app import db


# Objects Model
class Object(db.Model):
    __tablename__ = "object"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Object {self.name}>"
