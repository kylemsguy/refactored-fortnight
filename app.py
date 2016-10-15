from flask import Flask, redirect, request, session, render_template
from utils.validate_login import valid_login, log_the_user_in


app = Flask(__name__)


@app.route('/')
def index():
    if 'username' in session:
        return render_template('')
    return render_template('login.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['user'],
                       request.form['pass']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'
    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


if __name__ == '__main__':
    app.run()
