# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Fix tracking columns (SLOW!)

Create Date: 2016-08-04 09:56:42.330812
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from ggrc.migrations.utils.fix_tracking_columns import (
    upgrade_tables,
    downgrade_tables,
)


# revision identifiers, used by Alembic.
revision = '395186a2d8'
down_revision = '50b3f0b2a002'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  upgrade_tables("ggrc_gdrive_integration")


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  downgrade_tables("ggrc_gdrive_integration")
