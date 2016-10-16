import uuid

from database import db
from sqlalchemy.dialects.postgresql import UUID

import flask_login

'''
Format of Slack's user query response
{
  "ok": true,
  "team": "Hack Western 3",
  "team_id": "<team_id>",
  "url": "https://hackwestern3.slack.com/",
  "user": "user",
  "user_id": "<uid>"
}
'''

class User(db.Model, flask_login.UserMixin):
    __tablename__ = 'users'

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False, default='hacker')
    slack_id = db.Column(db.String(), nullable=False)
    skill = db.Column(db.String(), nullable=False)
    team_id = db.Column(UUID, db.ForeignKey('teams.id'))

    def __init__(self, id, name, type, slack_id, skill):
        self.id = id
        self.name = name
        self.type = type
        self.slack_id = slack_id
        self.skill = skill

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False, unique=True)
    members = db.relationship("User")

class Hack(db.Model):
    __tablename__ = 'stats'

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID, db.ForeignKey('users.id'))

