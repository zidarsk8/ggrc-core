
"""Add workflow state

Revision ID: 4d00d05f9e84
Revises: 2608242ad8ea
Create Date: 2014-08-19 11:41:38.723368

"""

# revision identifiers, used by Alembic.
revision = '4d00d05f9e84'
down_revision = '2608242ad8ea'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.add_column(u'workflows', sa.Column(u'status',
                sa.String(length=250), nullable=True))

  op.add_column(u'workflows',
    sa.Column('recurrences', sa.Boolean(), nullable=False))

  op.execute("""
    UPDATE workflows
    SET status='Draft', recurrences=true
    """)

  # one_time workflows don't have recurrences
  op.execute("""
    UPDATE workflows
    SET recurrences=false
    WHERE frequency='one_time'
    """)

  # workflows with cycles are active
  op.execute("""
    UPDATE workflows w
    INNER JOIN cycles c ON c.workflow_id = w.id
    SET w.status='Active'
    """)

  # but one_time workflows with cycles are inactive
  op.execute("""
    UPDATE workflows w
    INNER JOIN cycles c ON c.workflow_id = w.id
    SET w.status='Inactive'
    WHERE w.frequency='one_time'
    """)


def downgrade():
  op.drop_column(u'workflows', u'status')
  op.drop_column(u'workflows', u'recurrences')
