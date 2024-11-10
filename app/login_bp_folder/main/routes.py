# In your auth blueprint or where your login route is
from flask import render_template, redirect, url_for, flash
from app.signup_bp_folder.main.models.company_model import Company
from .forms import LoginForm
from .. import login_bp
from database import db
from flask_login import login_user, logout_user


@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        company_email = form.company_email.data
        pword = form.pword.data

        company_obj = db.session.query(Company).filter_by(email=company_email).first()

        if company_obj and company_obj.check_pword(pword):
            login_user(company_obj)  # Flask-Login will handle user session
            return redirect(url_for('homepage_bp.homepage'))
        else:
            flash('Login failed. Check your username and password.')

    return render_template('login_page.html', form=form)

@login_bp.route('/logout')
def logout():
    logout_user()  # This will log out the current user
    return redirect(url_for('login_bp.login'))
