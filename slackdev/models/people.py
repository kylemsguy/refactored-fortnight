import uuid

from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
from sqlalchemy.orm import relationship
from db import Base

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

class User(Base):
    __tablename__ = 'users'

    id = sa.Column(UUID, primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(), nullable=False)
    type = sa.Column(sa.String(), nullable=False, default='hacker')
    slack_id = sa.Column(sa.String(), nullable=False)
    skill = sa.Column(sa.String(), nullable=False)
    team_id = sa.Column(UUID, sa.ForeignKey('teams.id'))
    tutorial_status = sa.Column(sa.Integer(), nullable=False, default=0)

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

class Team(Base):
    __tablename__ = 'teams'

    id = sa.Column(UUID, primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(), nullable=False, unique=True)
    members = relationship("User")

class Hack(Base):
    __tablename__ = 'stats'

    id = sa.Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = sa.Column(UUID, sa.ForeignKey('users.id'))
