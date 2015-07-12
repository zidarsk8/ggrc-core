# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com


from ggrc import db
from ggrc.converters import errors
from ggrc.converters.handlers import UserColumnHandler
from ggrc.login import get_current_user
from ggrc_basic_permissions.models import Role
from ggrc_basic_permissions.models import UserRole


class UserRoleColumnHandler(UserColumnHandler):

  role_id = -1

  def parse_item(self):
    owners = set()
    email_lines = self.raw_value.splitlines()
    owner_emails = filter(unicode.strip, email_lines)  # noqa
    for raw_line in owner_emails:
      email = raw_line.strip().lower()
      person = self.get_person(email)
      if person:
        owners.add(person)
      else:
        self.add_warning(errors.UNKNOWN_USER_WARNING, email=email)

    if not owners:
      self.add_warning(errors.OWNER_MISSING)
      owners.add(get_current_user())

    return list(owners)

  def set_obj_attr(self):
    pass

  def get_value(self):
    emails = [owner.email for owner in self.row_converter.obj.owners]
    return "\n".join(emails)

  def remove_current_roles(self):
    UserRole.query.filter_by(
        role_id=self.role_id,
        context_id=self.row_converter.obj.context_id).delete()

  def insert_object(self):
    if self.dry_run or not self.value:
      return
    self.remove_current_roles()
    for owner in self.value:
      user_role = UserRole(
          role_id=self.role_id,
          context_id=self.row_converter.obj.context_id,
          person_id=owner.id
      )
      db.session.add(user_role)
    db.session.flush()


class ProgramOwnerColumnHandler(UserRoleColumnHandler):

  def __init__(self, row_converter, key, **options):
    self.role_id = Role.query.filter_by(name="ProgramOwner").one().id
    super(self.__class__, self).__init__(row_converter, key, **options)


class ProgramEditorColumnHandler(UserRoleColumnHandler):

  def __init__(self, row_converter, key, **options):
    self.role_id = Role.query.filter_by(name="ProgramEditor").one().id
    super(self.__class__, self).__init__(row_converter, key, **options)


class ProgramReaderColumnHandler(UserRoleColumnHandler):

  def __init__(self, row_converter, key, **options):
    self.role_id = Role.query.filter_by(name="ProgramReader").one().id
    super(self.__class__, self).__init__(row_converter, key, **options)


COLUMN_HANDLERS = {
    "program_owner": ProgramOwnerColumnHandler,
    "program_editor": ProgramEditorColumnHandler,
    "program_reader": ProgramReaderColumnHandler,
}
