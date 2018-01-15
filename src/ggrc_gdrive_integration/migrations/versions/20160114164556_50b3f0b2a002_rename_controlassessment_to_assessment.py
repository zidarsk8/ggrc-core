# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Rename ControlAssessment to Assessment

Revision ID: 50b3f0b2a002
Revises: 1511701c7ccc
Create Date: 2016-01-14 16:45:56.370769

"""

# revision identifiers, used by Alembic.
revision = '50b3f0b2a002'
down_revision = '1511701c7ccc'

from alembic import op

def upgrade():
  # Migrate all possible mappings where object_type = 'ControlAssessment'
  objects = {
      "object_folders": ("folderable_type",),
      "object_files": ("fileable_type",),
      "object_events": ("eventable_type",),
  }
  for key, values in objects.iteritems():
    for value in values:
      sql = """UPDATE {key} SET {value} = 'Assessment'
               WHERE {value} = 'ControlAssessment'"""
      op.execute(sql.format(key=key, value=value))

def downgrade():
  pass
