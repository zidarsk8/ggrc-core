# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Remove old notifications

Revision ID: 4dd6fbbc31fa
Revises: 56bda17c92ee
Create Date: 2015-04-01 15:57:02.080061

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4dd6fbbc31fa'
down_revision = '5180ce718082'


def upgrade():
  op.drop_table('notification_objects')
  op.drop_table('notification_recipients')
  op.drop_table('notifications')


def downgrade():
  op.create_table(
    'notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('context_id', sa.Integer(), nullable=True),
    sa.Column('notif_date', sa.DateTime(), nullable=True),
    sa.Column('notif_pri', sa.Integer, nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('subject', sa.Text(), nullable=True),
    sa.Column('sender_id', sa.Integer, nullable=False),
    sa.ForeignKeyConstraint(['context_id'], ['contexts.id'],),
    sa.ForeignKeyConstraint(['sender_id'], ['people.id'],),
    sa.PrimaryKeyConstraint('id')
  )

  op.create_table(
    'notification_objects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('context_id', sa.Integer(), nullable=True),
    sa.Column('notification_id', sa.Integer, nullable=False),
    sa.Column('object_id', sa.Integer, nullable=False),
    sa.Column('object_type', sa.String(length=250), nullable=False),
    sa.ForeignKeyConstraint(['context_id'], ['contexts.id'],),
    sa.ForeignKeyConstraint(['notification_id'], ['notifications.id'],),
    sa.PrimaryKeyConstraint('id')
  )

  op.create_table(
    'notification_recipients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=250), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_by_id', sa.Integer(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('context_id', sa.Integer(), nullable=True),
    sa.Column('notif_type', sa.String(length=250), nullable=True),
    sa.Column('notification_id', sa.Integer, nullable=False),
    sa.Column('recipient_id', sa.Integer, nullable=False),
    sa.Column('error_text', sa.Text, nullable=True),
    sa.Column('status', sa.String(length=250), nullable=True),
    sa.ForeignKeyConstraint(['context_id'], ['contexts.id'],),
    sa.ForeignKeyConstraint(['notification_id'], ['notifications.id'],),
    sa.ForeignKeyConstraint(['recipient_id'], ['people.id'],),
    sa.PrimaryKeyConstraint('id')
  )

