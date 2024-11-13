from wtforms_alchemy import ModelForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models.company_model import Company  # Update to your actual import path

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        # Exclude hashed password field, we’ll handle it separately
        exclude = ['pword']
        # Set the session, if needed, to access the database context for validation

    email = StringField(validators=[DataRequired(), Email(), Length(max=255)])
    phone_number = StringField(validators=[DataRequired(), Length(max=20)])
    form_pword = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_form_pword = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6), EqualTo('form_pword')])

