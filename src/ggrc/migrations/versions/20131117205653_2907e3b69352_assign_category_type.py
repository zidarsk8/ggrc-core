# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Assign Category types

Revision ID: 2907e3b69352
Revises: 22d3f8f2494c
Create Date: 2013-11-17 20:56:53.664719

"""

# revision identifiers, used by Alembic.
revision = '2907e3b69352'
down_revision = '22d3f8f2494c'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
import datetime


categories = [
    'Org and Admin/Governance',
      'Training',
      'Policies & Procedures',
      'HR',

    'Logical Access/ Access Control',
      'Access Management',
      'Authorization',
      'Authentication',

    'Change Management',
      'Segregation of Duties',
      'Configuration Management',
      'Package Verification and Code release',

    'Incident Management',
      'Monitoring ',
      'Process',

    'Business Continuity',
      'Disaster Recovery',
      'Restoration Tests',
      'Backup Logs ',
      'Replication',
      'Data Protection and Retention',

    'Physical Security',
      'Data Centers',
      'Sites',
    ]


assertions = [
    'Confidentiality',
    'Integrity',
    'Availability',
    'Security',
    'Privacy',
    ]


categories_table = table('categories',
    column('id', sa.Integer),
    column('type', sa.String),
    column('name', sa.String),
    column('parent_id', sa.Integer),
    column('scope_id', sa.Integer),
    column('modified_by_id', sa.Integer),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime),
    column('required', sa.Boolean),
    column('context_id', sa.Integer),
    )


categorizations_table = table('categorizations',
    column('id', sa.Integer),
    )


def upgrade():
    op.drop_constraint('categories_ibfk_1', 'categories', type_='foreignkey')

    # Clear Categorizations
    op.execute(categorizations_table.delete())
    op.execute(categories_table.delete())

    # Recreate categories and options
    timestamp = datetime.datetime.now()
    assertions_rows = [
        { 'type': 'ControlAssertion', 'name': value, 'scope_id': 102,
          'created_at': timestamp, 'updated_at': timestamp, 'context_id': None
          }
        for value in assertions
        ]
    categories_rows = [
        { 'type': 'ControlCategory', 'name': value, 'scope_id': 100,
          'created_at': timestamp, 'updated_at': timestamp, 'context_id': None
          }
        for value in categories
        ]
    op.bulk_insert(categories_table, assertions_rows)
    op.bulk_insert(categories_table, categories_rows)


def downgrade():
    # Clear Categorizations
    op.execute(categorizations_table.delete())
    op.execute(categories_table.delete())
    op.create_foreign_key('categories_ibfk_1', 'categories', 'categories', ['parent_id'], ['id'])
