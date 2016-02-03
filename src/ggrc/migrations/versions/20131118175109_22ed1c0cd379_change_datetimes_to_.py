# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Change datetimes to dates

Revision ID: 22ed1c0cd379
Revises: 2907e3b69352
Create Date: 2013-11-18 17:51:09.451933

"""

# revision identifiers, used by Alembic.
revision = '22ed1c0cd379'
down_revision = '2907e3b69352'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


timeboxed_tables = [
    'audits',
    'controls',
    'data_assets',
    'directives',
    'facilities',
    'markets',
    'object_controls',
    'object_documents',
    'object_objectives',
    'object_people',
    'object_sections',
    'org_groups',
    'products',
    'programs',
    'projects',
    'risks',
    'risky_attributes',
    'systems',
    ]

def upgrade():
    for table_name in timeboxed_tables:
      op.alter_column(table_name, u'start_date', existing_type=sa.DateTime(), type_=sa.Date(), nullable=True)
      op.alter_column(table_name, u'end_date', existing_type=sa.DateTime(), type_=sa.Date(), nullable=True)


def downgrade():
    for table_name in timeboxed_tables:
      op.alter_column(table_name, u'start_date', type_=sa.DateTime(), existing_type=sa.Date(), nullable=True)
      op.alter_column(table_name, u'end_date', type_=sa.DateTime(), existing_type=sa.Date(), nullable=True)
