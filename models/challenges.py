import uuid

from app import db
from sqlalchemy.dialects.postgresql import JSON, UUID


class Challenge(db.Model):
    __tablename__ = 'challenges'

    id = db.Column(UUID, primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    mentor_id = db.Column(UUID, db.ForeignKey('teams.id'), db.CheckConstraint('teams.type = \'mentor\''))