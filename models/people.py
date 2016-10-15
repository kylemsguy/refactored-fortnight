import uuid

from database import db
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False, default='hacker')
    slack_id = db.Column(db.String(), nullable=False)
    skill = db.Column(db.String(), nullable=False)
    team_id = db.Column(UUID, db.ForeignKey('teams.id'))

    def __init__(self, id, name, slack_id, skill):
        self.id = id
        self.name = name
        self.slack_id = slack_id
        self.skill = skill

    def __repr__(self):
        return '<id {}>'.format(self.id)


class Team(db.Model):
    __tablename__ = 'teams'

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    members = db.relationship("User")
