from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models.company_model import Company  # Update to your actual import path

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        # Exclude hashed password field, we’ll handle it separately
        exclude = ['pword']
        # Set the session, if needed, to access the database context for validation

    form_pword = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_form_pword = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6), EqualTo('form_pword')])
    submit = SubmitField('Signup')

