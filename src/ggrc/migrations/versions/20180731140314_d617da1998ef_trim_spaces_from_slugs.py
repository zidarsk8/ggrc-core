# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
trim spaces from slugs

Create Date: 2018-07-31 14:03:14.421240
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name, duplicate-code

from ggrc.migrations.utils.strip_text_field import \
    strip_text_field_ensure_unique

# revision identifiers, used by Alembic.
revision = 'd617da1998ef'
down_revision = '586c9b0bbebd'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""

  tables_with_slug = {
      'access_groups', 'assessment_templates', 'assessments', 'audits',
      'clauses', 'controls', 'data_assets', 'directives', 'documents',
      'evidence', 'facilities', 'issues', 'markets', 'metrics', 'objectives',
      'org_groups', 'products', 'programs', 'projects', 'sections',
      'systems', 'vendors',
  }
  strip_text_field_ensure_unique(tables_with_slug, 'slug')


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  pass
