from database import db
# Cameras Model
class Camera(db.Model):
    __tablename__ = 'cameras'

    camera_id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(255), unique=True, nullable=False)
    physical_location = db.Column(db.String(50), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    
    company = db.relationship('Company', backref='cameras')

    def __repr__(self):
        return f"<Camera {self.serial_number}>"