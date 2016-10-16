import uuid

from sqlalchemy.dialects.postgresql import JSON, UUID
import sqlalchemy as sa
from db import Base

class Challenge(Base):
    __tablename__ = 'challenges'

    id = sa.Column(UUID, primary_key=True, default=uuid.uuid4)
    name = sa.Column(sa.String(), nullable=False)
    mentor_id = sa.Column(UUID, sa.ForeignKey('teams.id'), sa.CheckConstraint('teams.type = \'mentor\''))
