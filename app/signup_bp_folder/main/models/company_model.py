from database import db

class Company(db.Model):
    __tablename__ = 'companies'  # Matches the existing Oracle table name

    company_id = db.Column(db.Integer, primary_key=True)  # Primary key, auto-incremented by Oracle sequence/trigger
    company_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    pword = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)

    def __init__(self, company_name, email, pword, phone_number):
        self.company_name = company_name
        self.email = email
        self.pword = pword
        self.phone_number = phone_number

    def __repr__(self):
        return f"<Company {self.company_name}>"