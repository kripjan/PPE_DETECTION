# In your auth blueprint or where your login route is
from flask import render_template, redirect, url_for, flash
from app.signup_bp_folder.main.models.company_model import Company
from .forms import LoginForm
from .. import login_bp
from database import db

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        company_name = form.username.data
        pword = form.pword.data
        
        company_obj = db.session.query(Company).filter_by(company_name=company_name).first()
        
        if company_obj and company_obj.check_password(pword):
            return redirect(url_for('homepage_bp.homepage'))
        else:
            flash('Login failed. Check your username and password.')

    return render_template('login_page.html', form=form)
