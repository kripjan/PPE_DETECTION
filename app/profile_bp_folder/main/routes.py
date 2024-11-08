# In your auth blueprint or where your profile route is
from flask import render_template, redirect, url_for, flash


@profile_bp.route('/profile', methods=['GET'])
def profile():
    

    return render_template('profile_page.html')
