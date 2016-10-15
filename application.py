# General Imports
import os

from flask import Flask, jsonify, g
from flask.ext.sqlalchemy import SQLAlchemy

import flask_login
import endpoints

from utils import errors, validate_login


def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def create_application():
    application = Flask(__name__)
    application.config['DEBUG'] = True # TODO TURN OFF ON PROD
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    application.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    application.config['SOCIAL_AUTH_USER_MODEL'] = 'models.people.User'
    application.config['SOCIAL_AUTH_SLACK_KEY'] = os.environ['SOCIAL_AUTH_SLACK_KEY']
    application.config['SOCIAL_AUTH_SLACK_SECRET'] = os.environ['SOCIAL_AUTH_SLACK_SECRET']
    application.config['SOCIAL_AUTH_AUTHENTICATION_BACKENDS'] = (
        'social.backends.slack.SlackOAuth2',
    )
    # set the secret key. So secret, it's an env var.
    application.secret_key = os.environ.get('SECRET_KEY')

    db = SQLAlchemy(application)
    db.init_app(application)
    application.register_blueprint(endpoints.utils.root, url_prefix='')
    application.register_blueprint(endpoints.utils.api, url_prefix='/api')
    application.register_error_handler(errors.InvalidUsage, handle_invalid_usage)
    return application

application = create_application()
login_manager = flask_login.LoginManager()
login_manager.init_app(application)

@login_manager.user_loader
def user_loader(uid):
    try:
        validate_login.get_user(uid)
    except Exception as e:
        import sys
        print(e, file=sys.stderr)
        raise e


if __name__ == '__main__':
    application.run()
