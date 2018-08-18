# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Add missing constraints for threats

Revision ID: 62f26762d0a
Revises: 2837682ad516
Create Date: 2015-11-12 16:10:29.579969

"""

from alembic import op
# from ggrc.migrations.utils.resolve_duplicates import resolve_duplicates
# from ggrc_risks.models import Threat

# revision identifiers, used by Alembic.
revision = '62f26762d0a'
down_revision = '2837682ad516'


def upgrade():
  # resolve_duplicates(Threat, 'slug')
  op.create_unique_constraint('uq_threats', 'threats', ['slug'])


def downgrade():
  op.drop_constraint('uq_threats', 'threats', 'unique')
