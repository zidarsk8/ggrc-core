# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Add options

Revision ID: 18e1e2aec298
Revises: 37c5ca51ad36
Create Date: 2013-11-16 23:50:30.637169

"""

# revision identifiers, used by Alembic.
revision = '18e1e2aec298'
down_revision = '37c5ca51ad36'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import datetime


options_table = table('options',
    column('id', sa.Integer),
    column('role', sa.String),
    column('title', sa.Text),
    column('description', sa.Text),
    column('modified_by_id', sa.Integer),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime),
    column('required', sa.Boolean),
    column('context_id', sa.Integer),
    )


options_values = [
    { 'role': 'network_zone', 'title': '3rd Party' },
    { 'role': 'network_zone', 'title': 'Core' },
    { 'role': 'network_zone', 'title': 'Service' },
    ]

changed_options_values = [
    { 'role': 'verify_frequency', 'old_title': 'Ad-Hoc', 'title': 'Bi-Weekly' },
    { 'role': 'verify_frequency', 'old_title': 'Bi-Annual', 'title': 'Bi-Monthly' },
    { 'role': 'verify_frequency', 'old_title': 'Semi-Annual', 'title': 'Semi-Annually' },
    { 'role': 'verify_frequency', 'old_title': 'Annual', 'title': 'Yearly' },
    ]


def upgrade():
    timestamp = datetime.datetime.now()

    connection = op.get_bind()
    for i, row in enumerate(options_values, start = 1):
      row = dict(row)
      connection.execute(options_table.insert().values(row))
    for i, row in enumerate(changed_options_values):
      row = dict(row)
      connection.execute(
          options_table.update().\
              where(
                sa.and_(
                  options_table.c.role == row['role'],
                  options_table.c.title == row['old_title']
                  )
              ).\
              values({ 'title': row['title'] }))


def downgrade():
    connection = op.get_bind()
    for i, row in enumerate(options_values, start = 1):
      row = dict(row)
      connection.execute(options_table.delete().where(
        sa.and_(
          options_table.c.role == row['role'],
          options_table.c.title == row['title']
          )
        ))
    for i, row in enumerate(changed_options_values):
      row = dict(row)
      connection.execute(
          options_table.update().\
              where(
                sa.and_(
                  options_table.c.role == row['role'],
                  options_table.c.title == row['title']
                  )
              ).\
              values({ 'title': row['old_title'] }))
