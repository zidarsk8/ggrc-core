## Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
## Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
## Created By: dan@reciprocitylabs.com
## Maintained By: dan@reciprocitylabs.com

"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision}
Create Date: ${create_date}

"""

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}

from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

def upgrade():
    ${upgrades if upgrades else "pass"}


def downgrade():
    ${downgrades if downgrades else "pass"}
