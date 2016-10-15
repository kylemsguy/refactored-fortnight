import os

from flask import Flask, redirect, request, session, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from utils.validate_login import valid_login, log_the_user_in, is_logged_in


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from models import people

@app.route('/')
def index():
    if is_logged_in():
        return render_template('main.html', user=session['username'])
    return render_template('login.html')


@app.route('/register', methods=['POST'])
def register():
    if not is_logged_in():
        pass


@app.route('/login', methods=['POST', 'GET'])
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


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect("/")


# set the secret key. So secret, it's an env var.
app.secret_key = os.environ.get('SECRET_KEY')


if __name__ == '__main__':
    app.run()
