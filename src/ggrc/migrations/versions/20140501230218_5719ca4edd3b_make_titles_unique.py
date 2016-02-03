# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Make titles unique in some cases.

Revision ID: 5719ca4edd3b
Revises: 16d7c239e894
Create Date: 2014-05-01 23:02:18.368434

"""

# revision identifiers, used by Alembic.
revision = '5719ca4edd3b'
down_revision = '16d7c239e894'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
  tables = [
    'audits',
    'controls',
    'data_assets',
    'directives',
    'facilities',
    'markets',
    'objectives',
    'org_groups',
    'products',
    'programs',
    'projects',
    'requests',
    'systems'
    ]

  for table in tables:
    op.execute(
      'create temporary table dupe_titles as select title from ' 
      + table 
      + ' group by title having count(*) > 1'
      )
    op.execute(
      'update ' 
      + table 
      + " set title=concat(title, ' (', id, ')' )"
      + 'where title in (select title from dupe_titles)'
    )
    op.execute(
      'drop table dupe_titles'
    )

  op.create_unique_constraint('uq_t_audits', 'audits', ['title'])
  op.create_unique_constraint('uq_t_controls', 'controls', ['title'])
  op.create_unique_constraint('uq_t_data_assets', 'data_assets', ['title'])
  op.create_unique_constraint('uq_t_directives', 'directives', ['title'])
  op.create_unique_constraint('uq_t_facilities', 'facilities', ['title'])
  op.create_unique_constraint('uq_t_markets', 'markets', ['title'])
  op.create_unique_constraint('uq_t_objectives', 'objectives', ['title'])
  op.create_unique_constraint('uq_t_org_groups', 'org_groups', ['title'])
  op.create_unique_constraint('uq_t_products', 'products', ['title'])
  op.create_unique_constraint('uq_t_programs', 'programs', ['title'])
  op.create_unique_constraint('uq_t_projects', 'projects', ['title'])
  op.create_unique_constraint('uq_requests', 'requests', ['slug'])
  op.create_unique_constraint('uq_t_systems', 'systems', ['title'])

def downgrade():
    op.drop_constraint('uq_t_systems', 'systems', 'unique')
    op.drop_constraint('uq_requests', 'requests', 'unique')
    op.drop_constraint('uq_t_projects', 'projects', 'unique')
    op.drop_constraint('uq_t_programs', 'programs', 'unique')
    op.drop_constraint('uq_t_products', 'products', 'unique')
    op.drop_constraint('uq_t_org_groups', 'org_groups', 'unique')
    op.drop_constraint('uq_t_objectives', 'objectives', 'unique')
    op.drop_constraint('uq_t_markets', 'markets', 'unique')
    op.drop_constraint('uq_t_facilities', 'facilities', 'unique')
    op.drop_constraint('uq_t_directives', 'directives', 'unique')
    op.drop_constraint('uq_t_data_assets', 'data_assets', 'unique')
    op.drop_constraint('uq_t_controls', 'controls', 'unique')
    op.drop_constraint('uq_t_audits', 'audits', 'unique')
