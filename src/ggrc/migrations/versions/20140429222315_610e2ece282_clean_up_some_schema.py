# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Clean up some schema artifacts

Revision ID: 610e2ece282
Revises: 3672c9261c8d
Create Date: 2014-04-29 22:23:15.992500

"""

# revision identifiers, used by Alembic.
revision = '610e2ece282'
down_revision = '3672c9261c8d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


def upgrade():
    op.alter_column('contexts', 'description',
               existing_type=mysql.TEXT(),
               nullable=True)
    op.alter_column('events', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('events', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.drop_constraint('meetings_ibfk_2', 'meetings', type_='foreignkey')
    op.drop_column('meetings', 'owner_id')
    op.alter_column('object_owners', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('object_owners', 'modified_by_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('object_owners', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('revisions', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=True)
    op.alter_column('revisions', 'modified_by_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('revisions', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=True)


def downgrade():
    op.alter_column('revisions', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('revisions', 'modified_by_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('revisions', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('object_owners', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('object_owners', 'modified_by_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('object_owners', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.add_column('meetings', sa.Column('owner_id', mysql.INTEGER(display_width=11), nullable=True))
    op.create_foreign_key(
        'meetings_ibfk_2', 'meetings', 'people', ['owner_id'], ['id'])
    op.alter_column('events', 'updated_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('events', 'created_at',
               existing_type=mysql.DATETIME(),
               nullable=False)
    op.alter_column('contexts', 'description',
               existing_type=mysql.TEXT(),
               nullable=False)
