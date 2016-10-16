import uuid

from flask import session, redirect, url_for, flash

from database import db
from models import people
from utils import errors


def valid_login(username, password):
    # TODO Implement
    return username and password


def register_or_login(slack_id):
    # Check if the user is already in the database
    q = people.User.query
    q = q.filter_by(slack_id=slack_id)

    result = q.first()

    if not result:
        return redirect(url_for('register'))

    return result


def get_user(uid):
    """Returns the currently logged in user"""
    uid = uuid.UUID(uid)
    model = people.User.query.filter_by(id=uid).first()
    if not model:
        return None
    return model