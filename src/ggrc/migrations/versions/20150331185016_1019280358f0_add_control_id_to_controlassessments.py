
"""add control_id to ControlAssessments

Revision ID: 1019280358f0
Revises: 19471f93d42
Create Date: 2015-03-31 18:50:16.859278

"""

# revision identifiers, used by Alembic.
revision = '1019280358f0'
down_revision = '19471f93d42'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('control_assessments', sa.Column('control_id', sa.Integer(), nullable=True))
    op.create_foreign_key('fk_control_control_assessment', 'control_assessments', 'controls', ['control_id'], ['id'])

def downgrade():
    op.drop_column('control_assessments', 'control_id')
    op.drop_constraint('fk_control_control_assessment', 'control_assessments', 'controls')
