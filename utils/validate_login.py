import uuid

from flask import session, redirect, url_for, flash

from flask_login import login_user

from database import db
from models import people
from utils import errors


def login_user(slack_id):
    # Check if the user is already in the database
    q = people.User.query
    q = q.filter_by(slack_id=slack_id)

    result = q.first()

    if not result:
        return None

    login_user(result)

    return result


def register_user(userdata):
    new_user = people.User()


def get_user(uid):
    """Returns the currently logged in user"""
    uid = uuid.UUID(uid)
    model = people.User.query.filter_by(id=uid).first()
    if not model:
        return None
    return model