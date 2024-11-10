# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    company_email = StringField('Company Email', validators=[DataRequired(), Email()])
    pword = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

