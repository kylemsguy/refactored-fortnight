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


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True # TODO TURN OFF ON PROD
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    app.config['SOCIAL_AUTH_USER_MODEL'] = 'models.people.User'
    app.config['SOCIAL_AUTH_SLACK_KEY'] = os.environ['SOCIAL_AUTH_SLACK_KEY']
    app.config['SOCIAL_AUTH_SLACK_SECRET'] = os.environ['SOCIAL_AUTH_SLACK_SECRET']
    app.config['SOCIAL_AUTH_AUTHENTICATION_BACKENDS'] = (
        'social.backends.slack.SlackOAuth2',
    )
    # set the secret key. So secret, it's an env var.
    app.secret_key = os.environ.get('SECRET_KEY')

    db = SQLAlchemy(app)
    db.init_app(app)
    app.register_blueprint(endpoints.utils.root, url_prefix='')
    app.register_blueprint(endpoints.utils.api, url_prefix='/api')
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


if __name__ == '__main__':
    app.run()
