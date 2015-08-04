# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Convert escaped title content to unescaped

Revision ID: 2ab3ec6c8f2
Revises: 5719ca4edd3b
Create Date: 2014-05-05 20:26:43.802693

"""
# this would ideally be a repeatable migration
# but as far as I know we do not support those
# with our current migrations structure. --BM

# revision identifiers, used by Alembic.
revision = '2ab3ec6c8f2'
down_revision = '5719ca4edd3b'

from alembic import op
from sqlalchemy.sql import table, column, func
import sqlalchemy as sa
from HTMLParser import HTMLParser
import bleach

def titled_table(tablename, singular):
  t = table(tablename,
      column('id', sa.Integer),
      column('title', sa.String),
      )
  t.singular_name = singular
  return t

# copied from src/ggrc/models/__init__.py
bleach_tags = [
    'caption', 'strong', 'em', 'b', 'i', 'p', 'code', 'pre', 'tt', 'samp',
    'kbd', 'var', 'sub', 'sup', 'dfn', 'cite', 'big', 'small', 'address',
    'hr', 'br', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul',
    'ol', 'li', 'dl', 'dt', 'dd', 'abbr', 'acronym', 'a', 'img',
    'blockquote', 'del', 'ins', 'table', 'tbody', 'tr', 'td', 'th',
    ] + bleach.ALLOWED_TAGS
bleach_attrs = {}
def cleaner(value):
  # Some cases like Request don't use the title value
  #  and it's nullable, so check for that
  if value is None:
    return value

  parser = HTMLParser()
  lastvalue = value
  value = parser.unescape(value)
  while value != lastvalue:
    lastvalue = value
    value = parser.unescape(value)

  ret = parser.unescape(
    bleach.clean(value, bleach_tags, bleach_attrs, strip=True)
    )
  return ret

titled_table_names = [
    ('audits', 'Audit'),
    ('controls', 'Control'),
    ('data_assets', 'Help'),
    ('directives', 'Directive'),
    ('documents', 'Document'),
    ('facilities', 'Facility'),
    ('helps', 'Help'),
    ('markets', 'Market'),
    ('meetings', 'Meeting'),
    ('objectives', 'Objective'),
    ('org_groups', 'OrgGroup'),
    ('products', 'Product'),
    ('programs', 'Program'),
    ('projects', 'Project'),
    ('sections', 'Section'),
    ('systems', 'System'),
    ]

titled_tables = [titled_table(*t) for t in titled_table_names]


def upgrade():
  conn = op.get_bind()
  for t in titled_tables:
    table_values = conn.execute(sa.select([t.c.id, t.c.title])).fetchall()

    for id, _title in table_values:
      clean_title = cleaner(_title)
      if clean_title != _title:
        op.execute(t.update()\
            .where(t.c.id == id)\
            .values(title=clean_title)
          )

def downgrade():
  pass
