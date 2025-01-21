from flask import flash
from app import db
from app.models.company import Company
from sqlalchemy.exc import IntegrityError, DataError, OperationalError
from flask_login import login_user


def register_company(form):
    """Register a new company in the database."""
    company_name = form.name.data
    email = form.email.data
    pword = form.form_pword.data
    phone_number = form.phone_number.data

    new_company = Company(company_name, email, pword, phone_number)

    try:
        db.session.add(new_company)
        db.session.commit()
        return True
    except IntegrityError:
        db.session.rollback()
        flash(
            "A company with this email already exists. Please try a different email.",
            "error",
        )
    except DataError:
        db.session.rollback()
        flash("Invalid data provided. Please check your inputs and try again.", "error")
    except OperationalError:
        db.session.rollback()
        flash("Database connection error. Please try again later.", "error")
    return False


def authenticate_user(form):
    """Authenticate a user based on the form inputs."""
    company_email = form.email.data
    pword = form.pword.data

    company_obj = db.session.query(Company).filter_by(email=company_email).first()

    if company_obj and company_obj.check_pword(pword):
        login_user(company_obj)
        return True
    return False
