"""Initial user info

Revision ID: 43cdb01d7e20
Revises: None
Create Date: 2016-10-15 11:57:09.201884

"""

# revision identifiers, used by Alembic.
revision = '43cdb01d7e20'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.create_table(
        'teams',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('slack_id', sa.String(), nullable=False),
        sa.Column('skill', sa.String(), nullable=False),
        sa.Column('team_id', postgresql.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['team_id'], ['teams.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade():
    op.drop_table('users')
    op.drop_table('teams')
