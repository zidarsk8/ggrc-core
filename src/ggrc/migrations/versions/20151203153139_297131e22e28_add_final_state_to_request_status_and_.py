# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

"""Add final state to request status and rename Unstarted to Open

Revision ID: 297131e22e28
Revises: 18cbdd3a7fd9
Create Date: 2015-12-03 15:31:39.979333

"""

# pylint: disable=invalid-name,missing-docstring,wrong-import-position

from alembic import op

# revision identifiers, used by Alembic.
revision = '297131e22e28'
down_revision = '504f541411a5'


def upgrade():
  op.execute("""ALTER TABLE requests CHANGE status status ENUM("Unstarted","In Progress","Finished","Verified","Open","Final") NOT NULL;""")  # noqa
  op.execute("""UPDATE requests SET status="Open" WHERE status="Unstarted";""")
  op.execute("""ALTER TABLE requests CHANGE status status ENUM("Open","In Progress","Finished","Verified","Final") NOT NULL;""")  # noqa


def downgrade():
  op.execute("""ALTER TABLE requests CHANGE status status ENUM("Open","In Progress","Finished","Verified","Final","Unstarted") NOT NULL;""")  # noqa
  op.execute("""UPDATE requests SET status="Unstarted" WHERE status="Open";""")
  op.execute("""UPDATE requests SET status="Finished" WHERE status="Final";""")
  op.execute("""ALTER TABLE requests CHANGE status status ENUM("Unstarted","In Progress","Finished","Verified") NOT NULL;""")  # noqa
