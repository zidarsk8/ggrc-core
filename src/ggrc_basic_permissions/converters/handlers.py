# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com


from ggrc import db
from ggrc.converters import errors
from ggrc.converters.handlers import UserColumnHandler
from ggrc.login import get_current_user


class ProgramOwnerColumnHandler(UserColumnHandler):

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

  def insert_object(self):
    if self.dry_run or not self.value:
      return
    from ggrc_basic_permissions.models import UserRole
    from ggrc_basic_permissions.models import Role
    role = Role.query.filter_by(name="ProgramOwner").one()
    UserRole.query.filter_by(
        role_id=role.id, context_id=self.row_converter.obj.context_id).delete()
    for owner in self.value:
      user_role = UserRole(
          role_id=role.id,
          context_id=self.row_converter.obj.context_id,
          person_id=owner.id
      )
      db.session.add(user_role)
    db.session.flush()


class ProgramEditorColumnHandler(UserColumnHandler):

  def parse_item(self):
    pass

  def set_obj_attr(self):
    pass

  def get_value(self):
    pass

  def insert_object(self):
    pass


class ProgramReaderColumnHandler(UserColumnHandler):

  def parse_item(self):
    pass

  def set_obj_attr(self):
    pass

  def get_value(self):
    pass

  def insert_object(self):
    pass

COLUMN_HANDLERS = {
    "program_owner": ProgramOwnerColumnHandler,
    "program_editor": ProgramEditorColumnHandler,
    "program_reader": ProgramReaderColumnHandler,
}
