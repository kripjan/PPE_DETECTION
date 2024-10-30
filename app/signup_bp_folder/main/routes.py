# In your auth blueprint or where your login route is
from flask import render_template, redirect, url_for, flash
from .forms import SignupForm
from .. import signup_bp

@signup_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        phone_number = form.phone_number.data
        email = form.email.data
        pword = form.pword.data
        
        # Adding user to database
        # logic here

        flash('Registration successful!', 'success')
        return redirect(url_for('login_bp.login'))
    return render_template('signup_page.html', form=form)
