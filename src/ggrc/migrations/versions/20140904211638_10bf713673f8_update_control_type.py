# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""update_control_type

Revision ID: 10bf713673f8
Revises: 5509cd84a758
Create Date: 2014-09-04 21:16:38.675118

"""

# revision identifiers, used by Alembic.
revision = '10bf713673f8'
down_revision = '5509cd84a758'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column, select
from sqlalchemy.exc import IntegrityError
import datetime

timestamp = datetime.datetime.now()

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
      {'role': 'control_means', 'title': 'Manual - Segregation of Duties', 'required': None, 'created_at': timestamp, 'updated_at': timestamp, },      
    ]

def upgrade():
    connection = op.get_bind()
    for row in options_values:
      try:
        connection.execute(options_table.update().where(options_table.c.title=='Manual w Segregation of Duties' and options_table.c.role=='control_means').values(row))
      except IntegrityError:
        pass
def downgrade():
    pass
