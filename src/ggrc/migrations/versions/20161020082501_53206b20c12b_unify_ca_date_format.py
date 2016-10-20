# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Unify CA date format

Create Date: 2016-10-20 08:25:01.140510
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op


# revision identifiers, used by Alembic.
revision = '53206b20c12b'
down_revision = 'bb6fe8e14bb'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  connection = op.get_bind()

  # change M/DD/YYYY or M/D/YYYY into MM/DD/YYYY or MM/D/YYYY correspondigly
  connection.execute("""
      UPDATE custom_attribute_values AS cav JOIN
             custom_attribute_definitions AS cad ON
                 cav.custom_attribute_id = cad.id
      SET cav.attribute_value = CONCAT('0', cav.attribute_value)
      WHERE cad.attribute_type = 'Date' AND
            cav.attribute_value REGEXP '^[0-9]{1}/[0-9]{1,2}/[0-9]{4}$'
  """)

  # change MM/D/YYYY into MM/DD/YYYY
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

  # change MM/DD/YYYY into YYYY-MM-DD
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

  # change YYYY-MM-DD 00:00:00 to YYYY-MM-DD
  connection.execute("""
      UPDATE custom_attribute_values AS cav JOIN
             custom_attribute_definitions AS cad ON
                 cav.custom_attribute_id = cad.id
      SET cav.attribute_value = SUBSTR(cav.attribute_value, 1, 10)
      WHERE cad.attribute_type = 'Date' AND
            cav.attribute_value REGEXP
                '^[0-9]{4}-[0-9]{2}-[0-9]{2} 00:00:00$'
  """)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  connection = op.get_bind()

  # change YYYY-MM-DD into MM/DD/YYYY
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
