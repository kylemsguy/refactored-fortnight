# General Imports
import os

from flask import Flask, jsonify, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import login_user , logout_user , current_user , login_required

import flask_login

from social.apps.flask_app.routes import social_auth
from social.apps.flask_app.default.models import init_social

import endpoints

from utils import errors, validate_login


def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True # TODO TURN OFF ON PROD
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    app.config['SOCIAL_AUTH_USER_MODEL'] = 'models.people.User'
    # set the secret key. So secret, it's an env var.
    app.secret_key = os.environ.get('SECRET_KEY')

    db = SQLAlchemy(app)
    db.init_app(app)
    app.register_blueprint(endpoints.utils.root, url_prefix='')
    app.register_blueprint(endpoints.utils.api, url_prefix='/api')
    app.register_blueprint(social_auth)
    init_social(app, db)
    app.register_error_handler(errors.InvalidUsage, handle_invalid_usage)
    return app

app = create_app()
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(uid):
    try:
        validate_login.get_user(uid)
    except Exception as e:
        import sys
        print(e, file=sys.stderr)
        raise e

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user


@app.before_request
def global_user():
    g.user = current_user

if __name__ == '__main__':
    app.run()
