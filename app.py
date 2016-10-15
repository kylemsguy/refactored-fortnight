# General Imports
import os

from flask import Flask, redirect, request, session, render_template
from flask.ext.sqlalchemy import SQLAlchemy

import endpoints

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True # TODO TURN OFF ON PROD
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
    # set the secret key. So secret, it's an env var.
    app.secret_key = os.environ.get('SECRET_KEY')

    db = SQLAlchemy(app)
    db.init_app(app)
    app.register_blueprint(endpoints.utils.root, url_prefix='')
    app.register_blueprint(endpoints.utils.api, url_prefix='/api')
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
