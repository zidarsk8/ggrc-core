# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
remove asterisks from CADs and roles

Create Date: 2019-02-19 10:30:03.388132
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op

from ggrc.models import all_models


# revision identifiers, used by Alembic.
revision = 'a8a44ea42a2b91'
down_revision = '57b14cb4a7b4'


def update_name(row_id, name, field, table, connection):
  """Update fields in DB to remove symbol '*'"""
  new_name = _generate_new_name(name, field, table, connection)
  connection.execute(sa.text("""
    UPDATE {}
    SET {} = '{}'
    WHERE id = {};
  """.format(table, field, new_name, row_id)))


def _generate_new_name(original_name, column, table, connection):
  """Remove symbol '*' from name and add appendix if new name already exists"""
  new_name = original_name.replace('*', '')
  iterator = 0
  while is_exists(new_name, column, table, connection):
    iterator += 1
    new_name = "{}-{}".format(original_name.replace('*', ''), iterator)
  return new_name


def get_roles_to_update(connection):
  """Get list of all access control roles with symbol '*' in it"""
  res = connection.execute(sa.text("""
    SELECT id, {0}
    FROM {1}
    WHERE {0} like '%*%'
    AND internal = 0;
  """.format('name', all_models.AccessControlRole.__tablename__))).fetchall()
  return res


def get_attributes_to_update(connection):
  """Get list of all custom attribute definitions with symbol '*' in it"""
  res = connection.execute(sa.text("""
    SELECT id, {0}
    FROM {1}
    WHERE {0} like '%*%';
  """.format('title',
             all_models.CustomAttributeDefinition.__tablename__))).fetchall()
  return res


def is_exists(value, name, table, connection):
  """Check is column name with value exists in table"""
  result = connection.execute(sa.text("""
    SELECT *
    FROM {}
    WHERE {} = '{}';
  """.format(table, name, value))).fetchall()
  if result:
    return True
  return False


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  connection = op.get_bind()

  roles_to_update = get_roles_to_update(connection)
  for role in roles_to_update:
    update_name(role.id, role.name, 'name',
                all_models.AccessControlRole.__tablename__, connection)

  attributes_to_update = get_attributes_to_update(connection)
  for attribute in attributes_to_update:
    update_name(attribute.id, attribute.title,
                'title', all_models.CustomAttributeDefinition.__tablename__,
                connection)


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  raise NotImplementedError("Downgrade is not supported")
