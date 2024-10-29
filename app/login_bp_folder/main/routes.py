# In your auth blueprint or where your login route is
from flask import render_template, redirect, url_for, flash
from login_bp_folder.main.forms import LoginForm
from login_bp_folder import login_bp

@login_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        # Add your logic here to check username and password
        if username == 'correct_username' and password == 'correct_password':  # Replace with your logic
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Check your username and password.')

    return render_template('login.html', form=form)
