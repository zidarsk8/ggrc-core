# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Audit contexts need to reference the audit for implication scoping.

Revision ID: 1ae73ec7bbc0
Revises: 21fb97276ef6
Create Date: 2014-03-02 13:09:47.544694

"""

# revision identifiers, used by Alembic.
revision = '1ae73ec7bbc0'
down_revision = '21fb97276ef6'

from alembic import op
from datetime import datetime
from sqlalchemy.sql import table, column, select
import sqlalchemy as sa

contexts_table = table('contexts',
    column('id', sa.Integer),
    column('related_object_id', sa.Integer),
    column('related_object_type', sa.String),
    column('updated_at', sa.DateTime),
    column('modified_by_id', sa.Integer),
    )

audits_table = table('audits',
    column('id', sa.Integer),
    column('context_id', sa.Integer),
    )

programs_table = table('programs',
    column('id', sa.Integer),
    column('context_id', sa.Integer),
    )

def upgrade():
  op.execute(
    contexts_table.update()\
        .values(
            related_object_id=audits_table.c.id,
            related_object_type='Audit',
            )\
        .where(
            contexts_table.c.id == audits_table.c.context_id,
            ))
  op.execute(
    contexts_table.update()\
        .values(
            related_object_id=programs_table.c.id,
            related_object_type='Program',
            )\
        .where(
            contexts_table.c.id == programs_table.c.context_id,
            ))


def downgrade():
  pass
