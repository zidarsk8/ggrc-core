
"""Add Issues

Revision ID: 19471f93d42
Revises: 56bda17c92ee
Create Date: 2015-03-27 16:46:53.627287

"""

# revision identifiers, used by Alembic.
revision = '19471f93d42'
down_revision = '56bda17c92ee'

from alembic import op
import sqlalchemy as sa


def upgrade():
  op.create_table(
      'issues',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('os_state', sa.String(length=250), nullable=False),
      sa.Column('test_plan', sa.Text(), nullable=True),
      sa.Column('end_date', sa.Date(), nullable=True),
      sa.Column('start_date', sa.Date(), nullable=True),
      sa.Column('status', sa.String(length=250), nullable=True),
      sa.Column('notes', sa.Text(), nullable=True),
      sa.Column('description', sa.Text(), nullable=True),
      sa.Column('url', sa.String(length=250), nullable=True),
      sa.Column('reference_url', sa.String(length=250), nullable=True),
      sa.Column('secondary_contact_id', sa.Integer(), nullable=True),
      sa.Column('contact_id', sa.Integer(), nullable=True),
      sa.Column('title', sa.String(length=250), nullable=False),
      sa.Column('slug', sa.String(length=250), nullable=False),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['contact_id'], ['people.id'], ),
      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], ),
      sa.ForeignKeyConstraint(['secondary_contact_id'], ['people.id'], ),
      sa.PrimaryKeyConstraint('id'),
      sa.UniqueConstraint('slug', name='uq_issues'),
      sa.UniqueConstraint('title', name='uq_t_issues')
  )


def downgrade():
  op.drop_table('issues')
