# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
migrate urls to documents

Create Date: 2017-05-02 14:06:36.936410
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name


# revision identifiers, used by Alembic.
revision = '377d935e1b21'
down_revision = '55f583313670'


HYPERLINKED_OBJECTS = {
    'Risk': 'risks',
    'Threat': 'threats'
}

HYPERLINKED_OBJ_TYPES = set(HYPERLINKED_OBJECTS)


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  # Document object is owned by ggrc, thus moved to ggrc migration chain
  pass


def downgrade():
  """Downgrade database schema and/or vdata back to the previous revision."""
  # Document object is owned by ggrc, thus moved to ggrc migration chain
  pass
