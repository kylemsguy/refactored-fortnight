from flask import session, render_template

from flask_login import login_required, logout_user, current_user

from endpoints.utils import root

@root.route('/')
def index():
    if current_user.is_authenticated():
        return render_template('dashboard.html', user=session['username'])
    else:
        session.clear()
        return render_template('login.html')
