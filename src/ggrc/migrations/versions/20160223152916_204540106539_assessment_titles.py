# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: ivan@reciprocitylabs.com
# Maintained By: ivan@reciprocitylabs.com

"""Assessment titles

Revision ID: 204540106539
Revises: 4e989ef86619
Create Date: 2016-02-23 15:29:16.361412

"""

# revision identifiers, used by Alembic.
revision = '204540106539'
down_revision = '4e989ef86619'

from alembic import op

from ggrc.models.assessment import Assessment
from ggrc.migrations.utils import resolve_duplicates


def upgrade():
  op.drop_constraint('uq_t_control_assessments', 'assessments', 'unique')

def downgrade():
  resolve_duplicates(Assessment, 'title', ' ')
  op.create_unique_constraint('uq_t_control_assessments', 'assessments', ['title'])
