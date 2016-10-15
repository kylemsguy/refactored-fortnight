from flask import session, render_template

from flask_login import login_required, logout_user

from endpoints.utils import root

from utils.validate_login import is_logged_in

@root.route('/')
def index():
    if is_logged_in():
        return render_template('main.html', user=session['username'])
    return render_template('login.html')
