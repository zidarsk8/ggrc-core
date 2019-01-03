# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Change format of fraud_related/key_control fields for existing proposals

Create Date: 2019-01-03 15:13:22.987617
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import json
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '077caaf74f6b'
down_revision = 'dd2a3a987de5'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  connection = op.get_bind()
  proposals_to_update = connection.execute(
      sa.text("""
          SELECT id, content
          FROM proposals
          WHERE instance_type='Control';
          """)).fetchall()
  for proposal in proposals_to_update:
    content = json.loads(proposal.content)
    # modify values for `key_control`
    if 'key_control' in content['fields']:
      if content['fields']['key_control'] == '1':
        content['fields']['key_control'] = True
      elif content['fields']['key_control'] == '0':
        content['fields']['key_control'] = False

    # modify values for `fraud_related`
    if 'fraud_related' in content['fields']:
      if content['fields']['fraud_related'] == '1':
        content['fields']['fraud_related'] = True
      elif content['fields']['fraud_related'] == '0':
        content['fields']['fraud_related'] = False

    connection.execute("""
       UPDATE proposals SET content='{}' WHERE id={};
     """.format(json.dumps(content), proposal.id))


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  pass
