# In your auth blueprint or where your profile route is
from flask import render_template, session, redirect, url_for, flash
from flask_login import current_user, login_required
from psutil import users
from app.blueprints.profile import profile
from app.models.company import Company
from flask import Blueprint


@profile.route("/profile/<int:company_id>", methods=["GET"])
@login_required
def profile_page(company_id):
    # Fetch the currently logged-in company details
    company = Company.query.get(current_user.id)

    if not company:
        return redirect(url_for("login_page.html"))  # Redirect if user is not found
    return render_template("profile_page.html", company=company)
