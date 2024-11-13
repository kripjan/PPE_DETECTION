# In your auth blueprint or where your login route is
from flask import render_template, redirect, url_for, flash
from app.models.company_model import Company
from app.blueprints.auth.forms.login_form import LoginForm
from app.blueprints.auth import auth
from app import db
from flask_login import login_user


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        company_email = form.company_email.data
        pword = form.pword.data

        company_obj = db.session.query(Company).filter_by(email=company_email).first()

        if company_obj and company_obj.check_pword(pword):
            login_user(company_obj)  # Flask-Login will handle user session
            return redirect(url_for('dashboard.homepage'))
        else:
            flash('Login failed. Check your username and password.')

    return render_template('login_page.html', form=form)
