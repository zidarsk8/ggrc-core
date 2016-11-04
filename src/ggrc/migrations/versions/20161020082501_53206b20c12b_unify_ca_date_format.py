# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Unify CA date format

Create Date: 2016-10-20 08:25:01.140510
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = '53206b20c12b'
down_revision = 'bb6fe8e14bb'


def _strip_whitespace_around_dates(connection):
  """Fix possibly existing dates prefixed with spaces in the DB."""

  dates = connection.execute("""
      SELECT cavs.id as id, attribute_value as value
      FROM custom_attribute_values AS cavs JOIN
           custom_attribute_definitions as cads ON
               cads.id = cavs.custom_attribute_id
      WHERE attribute_type = 'Date'
  """)

  for date in dates:
    if date.value is None:
      new_value = None
    else:
      new_value = date.value.strip()
    if date.value != new_value:
      connection.execute(text("""
          UPDATE custom_attribute_values SET
              attribute_value = :val
          WHERE id = :id
      """), val=new_value, id=date.id)


def _fix_single_digit_month(connection):
  """Change M/DD/YYYY (M/D/YYYY) into MM/DD/YYYY (MM/D/YYYY) correspondigly."""
  connection.execute("""
      UPDATE custom_attribute_values AS cav JOIN
             custom_attribute_definitions AS cad ON
                 cav.custom_attribute_id = cad.id
      SET cav.attribute_value = CONCAT('0', cav.attribute_value)
      WHERE cad.attribute_type = 'Date' AND
            cav.attribute_value REGEXP '^[0-9]{1}/[0-9]{1,2}/[0-9]{4}$'
  """)


def _fix_single_digit_day(connection):
  """Change MM/D/YYYY into MM/DD/YYYY."""
  connection.execute("""
      UPDATE custom_attribute_values AS cav JOIN
             custom_attribute_definitions AS cad ON
                 cav.custom_attribute_id = cad.id
      SET cav.attribute_value = CONCAT(SUBSTR(cav.attribute_value, 1, 3),
                                       '0',
                                       SUBSTR(cav.attribute_value, 4, 9))
      WHERE cad.attribute_type = 'Date' AND
            cav.attribute_value REGEXP '^[0-9]{2}/[0-9]{1}/[0-9]{4}$'
  """)


def _american_date_to_iso(connection):
  """Change MM/DD/YYYY into YYYY-MM-DD."""
  connection.execute("""
      UPDATE custom_attribute_values AS cav JOIN
             custom_attribute_definitions AS cad ON
                 cav.custom_attribute_id = cad.id
      SET cav.attribute_value = CONCAT_WS('-',
                                          SUBSTR(cav.attribute_value, 7, 4),
                                          SUBSTR(cav.attribute_value, 1, 2),
                                          SUBSTR(cav.attribute_value, 4, 2))
      WHERE cad.attribute_type = 'Date' AND
            cav.attribute_value REGEXP '^[0-9]{2}/[0-9]{2}/[0-9]{4}$'
  """)


def _strip_trailing_zero_time(connection):
  """Change YYYY-MM-DD 00:00:00 to YYYY-MM-DD."""
  connection.execute("""
      UPDATE custom_attribute_values AS cav JOIN
             custom_attribute_definitions AS cad ON
                 cav.custom_attribute_id = cad.id
      SET cav.attribute_value = SUBSTR(cav.attribute_value, 1, 10)
      WHERE cad.attribute_type = 'Date' AND
            cav.attribute_value REGEXP
                '^[0-9]{4}-[0-9]{2}-[0-9]{2} 00:00:00$'
  """)


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  connection = op.get_bind()

  _strip_whitespace_around_dates(connection)

  _fix_single_digit_month(connection)
  _fix_single_digit_day(connection)
  _american_date_to_iso(connection)

  _strip_trailing_zero_time(connection)


def _iso_date_to_american(connection):
  """Change YYYY-MM-DD into MM/DD/YYYY."""
  connection.execute("""
      UPDATE custom_attribute_values AS cav JOIN
             custom_attribute_definitions AS cad ON
                 cav.custom_attribute_id = cad.id
      SET cav.attribute_value = CONCAT_WS('/',
                                          SUBSTR(cav.attribute_value, 6, 2),
                                          SUBSTR(cav.attribute_value, 9, 2),
                                          SUBSTR(cav.attribute_value, 1, 4))
      WHERE cad.attribute_type = 'Date' AND
            cav.attribute_value REGEXP '^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
  """)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  connection = op.get_bind()

  _iso_date_to_american(connection)

