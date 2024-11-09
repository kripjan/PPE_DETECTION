# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])
    pword = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

