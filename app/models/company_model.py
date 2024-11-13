from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class Company(db.Model, UserMixin):
    __tablename__ = 'companies'

    company_id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    pword = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    def __init__(self, company_name, email, form_pword, phone_number):
        self.company_name = company_name
        self.email = email
        self.set_pword(form_pword)
        self.phone_number = phone_number

    def __repr__(self):
        return f"<Company {self.company_name}>"
    
    def set_pword(self, form_pword):
        self.pword = generate_password_hash(form_pword)

    def check_pword(self, form_pword):
        return check_password_hash(self.pword, form_pword)

    def get_id(self):
        return str(self.company_id)