from flask import session, render_template

from flask_login import login_required, logout_user

from endpoints.utils import root

@root.route('/')
def index():
    if False:
        return render_template('main.html', user=session['username'])
    return render_template('login.html')
