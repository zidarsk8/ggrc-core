# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Put ObjectObjective in the correct context for Program

Revision ID: 5509cd84a758
Revises: e09d8acc49b
Create Date: 2014-08-26 00:57:11.356427

"""

# revision identifiers, used by Alembic.
revision = '5509cd84a758'
down_revision = 'e09d8acc49b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute("""
      UPDATE object_objectives o
      INNER JOIN programs p ON o.objectiveable_id = p.id
      SET o.context_id = p.context_id
      WHERE o.objectiveable_type = 'Program'
      """)

def downgrade():
    # No going back
    pass
