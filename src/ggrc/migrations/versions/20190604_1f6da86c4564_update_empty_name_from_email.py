# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
update empty name from email

Create Date: 2019-06-04 11:35:57.993731
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op


# revision identifiers, used by Alembic.
revision = '1f6da86c4564'
down_revision = '437d91566937'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.execute("""
      UPDATE people
      SET name=SUBSTRING_INDEX(email, '@', 1) WHERE name=''
  """)

def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  raise NotImplementedError("Downgrade is not supported")
