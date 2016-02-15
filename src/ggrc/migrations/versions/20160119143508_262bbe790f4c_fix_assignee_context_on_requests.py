# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""Fix assignee context on requests

Revision ID: 262bbe790f4c
Revises: 297131e22e28
Create Date: 2016-01-19 14:35:08.577857

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = '262bbe790f4c'
down_revision = '297131e22e28'


def upgrade():
  # Make sure all requests have the audit context
  op.execute("""UPDATE requests AS r
                JOIN audits AS a ON r.audit_id = a.id
                SET r.context_id = a.context_id;""")
  # Set context_id where Request is source
  op.execute("""UPDATE relationships as rel
                JOIN requests AS req ON rel.source_id = req.id
                SET rel.context_id = req.context_id
                WHERE rel.source_type = 'Request'
                AND rel.destination_type = 'Person';""")
  # Set context_id where Request is destination
  op.execute("""UPDATE relationships as rel
                JOIN requests AS req ON rel.destination_id = req.id
                SET rel.context_id = req.context_id
                WHERE rel.destination_type = 'Request'
                AND rel.source_type = 'Person';""")


def downgrade():
  pass
