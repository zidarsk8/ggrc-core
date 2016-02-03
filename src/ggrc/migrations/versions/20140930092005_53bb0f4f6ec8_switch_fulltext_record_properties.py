# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""Switch fulltext_record_properties to innodb

Revision ID: 53bb0f4f6ec8
Revises: 63fc392c91a
Create Date: 2014-09-30 09:20:05.884100

"""

# revision identifiers, used by Alembic.
revision = '53bb0f4f6ec8'
down_revision = '63fc392c91a'

from alembic import op


def upgrade():
  op.drop_index('fulltext_record_properties_text_idx',
                table_name='fulltext_record_properties')
  op.execute("ALTER TABLE fulltext_record_properties ENGINE=InnoDB")


def downgrade():
  op.execute("""
      ALTER TABLE fulltext_record_properties
      ENGINE=MyISAM,
      ADD FULLTEXT INDEX `fulltext_record_properties_text_idx` (`content`)
  """)
