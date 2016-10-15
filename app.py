from flask import Flask, redirect, request, session, render_template


app = Flask(__name__)


@app.route('/')
def index():
    if 'username' in session:
        return render_template('')
    return render_template('login.html')

@app.route('/login')
def login():
    if request.

if __name__ == '__main__':
    app.run()
