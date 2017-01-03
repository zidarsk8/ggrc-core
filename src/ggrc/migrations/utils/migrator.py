# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
Migrator Utility Module.

Provides default user for migrations (migrator).  It is useful in migrations,
where user account is needed, but it is impossible to detect which user accout
should be used.

It uses ``MIGRATOR`` value from the ``ggrc.settings`` module. The value should
be user name in format ``User Name <email@example.com>``.

"""

from email.utils import parseaddr

# pylint: disable=invalid-name,
import sqlalchemy as sa
from alembic import op

from ggrc import settings


def ensure_user():
  """
  Ensure migrator account exists and return its ID.

  If migrator doesn't exists, a new one will be created using info from
  ``ggrc.settings.MIGRATOR``.

  """
  conn = op.get_bind()
  meta = sa.MetaData(bind=conn)
  people = sa.Table('people', meta, autoload=True)

  name, email = parseaddr(settings.MIGRATOR)
  if not email:
    raise ValueError('Invalid migrator email. '
                     'Check MIGRATOR value within settings')
  if not name:
    name = email

  user_id = sa.select([people.c.id]).where(people.c.email == email)
  user_id = conn.execute(user_id).scalar()
  if user_id is not None:
    return user_id

  result = conn.execute(
      people.insert().values(  # pylint: disable=no-value-for-parameter
          email=email,
          name=name,
          created_at=sa.sql.func.now(),
          updated_at=sa.sql.func.now(),
      )
  )
  return result.inserted_primary_key[0]
