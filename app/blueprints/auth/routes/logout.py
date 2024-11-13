# In your auth blueprint or where your login route is
from flask import render_template, redirect, url_for, flash
from app.models.company_model import Company
from app.blueprints.auth.forms.login_form import LoginForm
from app.blueprints.auth import auth
from app import db
from flask_login import logout_user

@auth.route('/logout')
def logout():
    logout_user()  # This will log out the current user
    return redirect(url_for('auth.login'))