# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""fresh start for notifications

Revision ID: 57cc398ad417
Revises: 49541e2c6db5
Create Date: 2015-04-01 15:57:32.952092

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '57cc398ad417'
down_revision = '49541e2c6db5'


def upgrade():

  op.create_table(
      'notification_types',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('name', sa.String(length=250), nullable=False),
      sa.Column('description', sa.String(length=250), nullable=True),
      sa.Column('advance_notice', sa.Integer(), nullable=True),
      sa.Column('template', sa.String(length=250), nullable=False),
      sa.Column('instant', sa.Boolean(), nullable=False, default=False),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['modified_by_id'], ['people.id'],),
      sa.PrimaryKeyConstraint('id')
  )

  op.create_table(
      'notifications',
      sa.Column('id', sa.Integer(), nullable=False),
      sa.Column('object_id', sa.Integer(), nullable=False),
      sa.Column('object_type_id', sa.Integer(), nullable=False),
      sa.Column('notification_type_id', sa.Integer(), nullable=False),
      sa.Column('send_on', sa.DateTime(), nullable=False),
      sa.Column('sent_at', sa.DateTime(), nullable=True),
      sa.Column('custom_message', sa.Text(), nullable=True),
      sa.Column(
          'force_notifications', sa.Boolean(), default=False, nullable=False),
      sa.Column('created_at', sa.DateTime(), nullable=True),
      sa.Column('modified_by_id', sa.Integer(), nullable=True),
      sa.Column('updated_at', sa.DateTime(), nullable=True),
      sa.Column('context_id', sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(['object_type_id'], ['object_types.id'],),
      sa.ForeignKeyConstraint(
          ['notification_type_id'], ['notification_types.id'],),
      sa.ForeignKeyConstraint(['modified_by_id'], ['people.id'],),
      sa.PrimaryKeyConstraint('id')
  )
  op.create_index('fk_notification_type_id', 'notifications', ['notification_type_id'],
                  unique=False)


def downgrade():
  op.drop_table('notifications')
  op.drop_table('notification_types')
