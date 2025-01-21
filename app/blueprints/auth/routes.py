from flask import render_template, redirect, url_for, flash
from flask_login import logout_user
from app.blueprints.auth.forms.company_form import CompanyForm
from app.blueprints.auth.forms.login_form import LoginForm
from app.blueprints.auth.services import *
from app.blueprints.auth import auth

# from app.models.company_model import Company
# from app import db


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = CompanyForm()
    if form.validate():
        if register_company(form):
            flash("Registration successful!", "success")
            return redirect(url_for("auth.login"))
    return render_template("signup_page.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if authenticate_user(form):
            return redirect(url_for("dashboard.home_page"))
        flash("Login failed. Check your username and password.", "error")
    return render_template("login_page.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
