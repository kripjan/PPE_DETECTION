from wtforms_alchemy import ModelForm
from wtforms import PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional
from app.models.company_model import Company  # Update to your actual import path
from app import db

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        # Exclude hashed password field, we’ll handle it separately
        exclude = ['pword']
        # Set the session, if needed, to access the database context for validation

    email = db.EmailField(validators=[DataRequired(), Email(), Length(max=255)])
    phone_number = db.StringField(validators=[DataRequired(), Length(max=20)])
    form_pword = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

