# In your auth blueprint or where your login route is
from sqlite3 import DataError, IntegrityError, OperationalError
from flask import render_template, redirect, url_for, flash
from app import db
from app.models.company_model import Company
from app.blueprints.auth import auth
from app.blueprints.auth.forms.company_form import CompanyForm

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = CompanyForm()
    if form.validate_on_submit():
        company_name = form.company_name.data
        email = form.email.data
        pword = form.pword.data
        phone_number = form.phone_number.data
        
        # creating a Company model object
        new_company = Company(company_name, email, pword, phone_number)

        try:
            db.session.add(new_company) # adding the new registered company details to the database
            db.session.commit() # committing the adding of those details (commit means saving the changes to the database)

            flash('Registration successful!', 'success') # flashing a success message to the html page
            return redirect(url_for('auth.login'))

        except IntegrityError: # if the entered email is already in use
            db.session.rollback()  # Undo the add operation and reset session state
            flash("A company with this email already exists. Please try a different email.", "error")

        except DataError: # if invalid data is entered in the form
            db.session.rollback()  # Undo any partial changes
            flash("Invalid data provided. Please check your inputs and try again.", "error")

        except OperationalError: # if there is some error with the database server
            db.session.rollback()  # Reset the session on database connection failure
            flash("Database connection error. Please try again later.", "error")

    return render_template('signup_page.html', form=form)
