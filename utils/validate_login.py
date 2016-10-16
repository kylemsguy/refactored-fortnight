import uuid

from flask import session, redirect, url_for, flash

from flask_login import login_user

from database import db
from models import people
from utils import errors


def check_user_exists(slack_id):
    # Check if the user is already in the database
    q = people.User.query
    q = q.filter_by(slack_id=slack_id)

    result = q.first()

    if not result:
        return None

    login_user(result)

    return result


def register_user(userdata, team_data=None):
    slack_data = session['new_user']
    new_user = people.User(
        id=uuid.uuid4(),
        name=slack_data['name'],
        type='hacker',
        slack_id=slack_data['user_id'],
        skill=userdata['skill'],
    )

    if team_data:
        new_team = people.Team()
        new_team.id = uuid.uuid4()
        new_team.name = team_data['name']

        new_user.team_id = new_team.id

        db.session.add(new_team)
    else:
        new_user.team_id = userdata['team_id']

    db.session.add(new_user)
    db.session.commit()

    login_user(new_user)

    return new_user


def get_user(uid):
    """Returns the currently logged in user"""
    uid = uuid.UUID(uid)
    model = people.User.query.filter_by(id=uid).first()
    if not model:
        return None
    return model