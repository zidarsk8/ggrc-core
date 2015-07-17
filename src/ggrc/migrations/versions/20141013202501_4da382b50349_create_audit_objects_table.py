# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Create audit_objects table

Revision ID: 4da382b50349
Revises: 51f6b61fd82a
Create Date: 2014-06-13 20:25:01.824560

"""

# revision identifiers, used by Alembic.
revision = '4da382b50349'
down_revision = '3a4ce23d81b0'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


def upgrade():
    op.create_table(u"audit_objects",
      sa.Column(u'id', sa.Integer(), nullable=False),
      sa.Column(u'modified_by_id', sa.Integer(), nullable=True),
      sa.Column(u'created_at', sa.DateTime(), nullable=True),
      sa.Column(u'updated_at', sa.DateTime(), nullable=True),
      sa.Column(u'context_id', sa.Integer(), nullable=False),
      sa.Column(u'audit_id', sa.Integer(), nullable=False),
      sa.Column(u'auditable_id', sa.Integer(), nullable=False),
      sa.Column(u'auditable_type', sa.String(length=250), nullable=False),

      sa.ForeignKeyConstraint(['context_id'], ['contexts.id'], ),
      sa.ForeignKeyConstraint(['audit_id'], ['audits.id'], ),
      sa.PrimaryKeyConstraint(u'id'),
      sa.UniqueConstraint(u'audit_id', u'auditable_id', u"auditable_type")
      )

    op.add_column(
      u'audits',
      sa.Column(u'object_type', sa.String(length=250), nullable=False)
      )

    audits_table = table('audits',
      column('id', sa.Integer),
      column('object_type', sa.String)
      )

    op.execute(audits_table.update()\
      .values(object_type=u'Objective')\
      )

def downgrade():
    op.drop_column(
      u'audits',
      u'object_type'
      )

    op.drop_table(u'audit_objects')
