# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Modify import_export table and update(compress) background task payload

Create Date: 2019-02-04 11:07:57.982626
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import pickle
import zlib

import sqlalchemy as sa
import sqlalchemy.types as types
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision = '25a1b9502690'
down_revision = '0d7a3a0aa3da'


class CompressedType(types.TypeDecorator):
  # pylint: disable=W0223
  """ Custom Compresed data type

  Custom type for storing any python object in our database as serialized text.
  """
  MAX_BINARY_LENGTH = 16777215
  impl = types.BLOB(length=MAX_BINARY_LENGTH)

  def process_result_value(self, value, dialect):
    if value is not None:
      value = pickle.loads(zlib.decompress(value))
    return value

  def process_bind_param(self, value, dialect):
    value = zlib.compress(pickle.dumps(value))
    if len(value) > self.MAX_BINARY_LENGTH:
      raise ValueError("Log record content too long")
    return value


def _compress_bg_tasks_payload():
  """Compress payload content of all backgroundtasks for compatibility"""
  connection = op.get_bind()

  uncompressed_payload = connection.execute(
      sa.text("""SELECT id, payload FROM background_tasks""")
  ).fetchall()
  for _id, payload in uncompressed_payload:
    if payload:
      connection.execute(
          sa.text(
              """UPDATE background_tasks
                 SET payload=:payload WHERE id=:id;"""
          ),
          payload=zlib.compress(payload),
          id=_id
      )


def _alter_import_export_table():
  """Alter content field of import_export table"""
  op.alter_column(
      'import_exports',
      'content',
      existing_type=mysql.LONGTEXT,
    type_=CompressedType(length=16777215)
  )


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  _compress_bg_tasks_payload()
  _alter_import_export_table()


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  raise NotImplementedError("Downgrade is not supported")
