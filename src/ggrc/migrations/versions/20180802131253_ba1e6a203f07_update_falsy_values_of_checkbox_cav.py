# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Update falsy values of Checkbox CAV

Create Date: 2018-08-02 13:12:53.218878
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from datetime import datetime
from alembic import op
from sqlalchemy.sql import text
from ggrc.migrations.utils.migrator import get_migration_user_id

# revision identifiers, used by Alembic.
revision = 'ba1e6a203f07'
down_revision = 'd617da1998ef'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  connection = op.get_bind()
  migration_user_id = get_migration_user_id(connection)
  current_datetime = datetime.now()

  op.execute("SET SESSION SQL_SAFE_UPDATES = 0")

  update_sql = """
      UPDATE custom_attribute_values AS cav
        JOIN custom_attribute_definitions AS cad
          ON cad.id = cav.custom_attribute_id
      SET cav.attribute_value = 0,
          cav.modified_by_id = :modified_by_id,
          cav.updated_at = :current_datetime
      WHERE cad.attribute_type = "Checkbox" and cav.attribute_value = "";
  """
  connection.execute(text(update_sql),
                     modified_by_id=migration_user_id,
                     current_datetime=current_datetime)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
