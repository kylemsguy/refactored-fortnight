from flask import request, render_template, redirect, session

from endpoints.utils import root
from utils.validate_login import valid_login, log_the_user_in, is_logged_in, create_user

@root.route('/register', methods=['POST'])
def register():
    if not is_logged_in():
        # register user
        pass


@root.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['user'],
                       request.form['pass']):
            return log_the_user_in(request.form['user'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


@root.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect("/")
