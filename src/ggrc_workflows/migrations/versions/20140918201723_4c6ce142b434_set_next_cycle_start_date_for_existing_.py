# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

"""set next cycle start date for existing workflows

Revision ID: 4c6ce142b434
Revises: 53dcddf6c09e
Create Date: 2014-09-18 20:17:23.080878

"""

# revision identifiers, used by Alembic.
revision = '4c6ce142b434'
down_revision = '53dcddf6c09e'

from datetime import date
from ggrc import settings, db
from alembic import op
import sqlalchemy as sa
import ggrc_workflows.models as models
from ggrc_workflows.models import *
from ggrc_workflows.models.mixins import RelativeTimeboxed

def upgrade():
  # Upgrade is no longer needed for fresh instances
  pass

def downgrade():
    pass
