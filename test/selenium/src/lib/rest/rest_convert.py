# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Conversions from App entity to REST."""
from lib.constants import roles

_APP_ACCESS_CONTROL_ROLE_MAPPING = {
    "admins": "Admin",
    "wf_members": "Workflow Member"
}


def build_access_control_list(obj):
  """Builds access_control_list from obj."""
  obj_type = obj.obj_type()
  access_control_list = []
  for key, value in obj.__dict__.iteritems():
    if key in _APP_ACCESS_CONTROL_ROLE_MAPPING:
      acr_name = _APP_ACCESS_CONTROL_ROLE_MAPPING[key]
      role_id = roles.ACLRolesIDs.id_of_role(
          object_type=obj_type, name=acr_name)
      access_control_list.extend(
          {"ac_role_id": role_id, "person": to_basic_rest_obj(person)}
          for person in value)
  return access_control_list


def to_basic_rest_obj(obj):
  """Return basic REST dict based on `obj`."""
  return {"type": obj.obj_type(), "id": obj.obj_id}


def default_context():
  """Returns default value for context."""
  return {"id": None}
