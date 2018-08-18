# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Fix tracking columns (SLOW!)

Create Date: 2016-07-28 14:29:21.825263
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from ggrc.migrations.utils.fix_tracking_columns import (
    upgrade_tables,
    downgrade_tables,
)


# revision identifiers, used by Alembic.
revision = '4cb78ab9a321'
down_revision = '4fa163aa5dc4'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  upgrade_tables("ggrc_workflows")


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  downgrade_tables("ggrc_workflows")
