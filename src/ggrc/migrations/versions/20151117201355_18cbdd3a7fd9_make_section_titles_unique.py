# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

"""Make section titles unique

Revision ID: 18cbdd3a7fd9
Revises: 27684e5f313a
Create Date: 2015-11-17 20:13:55.593299

"""

# revision identifiers, used by Alembic.
revision = '35e5344803b4'
down_revision = '27684e5f313a'

from alembic import op

from ggrc.models.section import Section
from ggrc.migrations.utils import resolve_duplicates


def upgrade():
  resolve_duplicates(Section, 'title', " ")
  op.create_unique_constraint('uq_t_sections', 'sections', ['title'])


def downgrade():
  op.drop_constraint('uq_t_sections', 'sections', 'unique')
