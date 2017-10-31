# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Collection of utils for login and user generation.
"""

from ggrc import db, settings
from ggrc.integrations import client
from ggrc.login import get_current_user_id
from ggrc.models.person import Person
from ggrc.rbac import SystemWideRoles
from ggrc.utils.log_event import log_event
from ggrc_basic_permissions import basic_roles
from ggrc_basic_permissions.models import UserRole


def _base_user_query():
  from sqlalchemy import orm
  return Person.query.options(
      orm.undefer_group('Person_complete'))


def find_user_by_id(user_id):
  """Find Person object by some ``id``.

  Note that ``id`` need not be Person().id, but should match the value
  returned by ``Person().get_id()``.
  """
  return _base_user_query().get(int(user_id))


def find_user_by_email(email):
  return _base_user_query().filter(Person.email == email).first()


def add_creator_role(user):
  """Add creator role for sent user."""
  user_creator_role = UserRole(
      person=user,
      role=basic_roles.creator(),
  )
  db.session.add(user_creator_role)
  db.session.commit()
  log_event(db.session, user_creator_role, user_creator_role.id)


def create_user(email, **kwargs):
  """Create User

  attr:
      email (string) required
  """
  user = Person(email=email, **kwargs)
  db.session.add(user)
  db.session.flush()
  log_event(db.session, user, user.id)
  db.session.commit()
  return user


def is_authorized_domain(email):
  """Check whether user's email belongs to authorized domain"""
  # Email can have multiple @, but last one separates local and domain part
  user_domain = email.split("@")[-1]
  return user_domain.lower() == settings.AUTHORIZED_DOMAIN.lower()


def find_or_create_user_by_email(email, name):
  """Generates or find user for selected email."""
  user = find_user_by_email(email)
  if not user:
    user = create_user(email,
                       name=name,
                       modified_by_id=get_current_user_id())
  if is_authorized_domain(email) and \
     user.system_wide_role == SystemWideRoles.NO_ACCESS:
    add_creator_role(user)
  return user


def search_user(email):
  """Search user by Integration Service

    Returns:
        string: user name for success, None otherwise
  """
  service = client.PersonClient()
  if is_authorized_domain(email):
    ldaps = service.search_persons([email.split("@")[0]])
    if ldaps:
      return "%s %s" % (ldaps[0]["firstName"], ldaps[0]["lastName"])
  return None


def find_or_create_external_user(email, name):
  """Find or generate user after verification"""
  if settings.INTEGRATION_SERVICE_URL and search_user(email):
    return find_or_create_user_by_email(email, name)
  return None
