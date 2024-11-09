from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class SignupForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    pword = PasswordField('Password', validators=[DataRequired()])
    confirm_pword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('pword')])
    submit = SubmitField('Sign Up')
