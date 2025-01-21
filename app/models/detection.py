from app import db
from sqlalchemy import LargeBinary


class Detection(db.Model):
    __tablename__ = "detection"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.TIMESTAMP, nullable=False)
    image_data = db.Column(LargeBinary, nullable=False)  # Column to store the image
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    company = db.relationship("Company", backref="detections")
