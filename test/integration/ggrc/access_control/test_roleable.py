# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Access Control Roleable mixin"""
import ddt
from ggrc import db
from ggrc.models import all_models
from ggrc.models.mixins import Identifiable
from ggrc.access_control import roleable
from integration.ggrc import TestCase
from integration.ggrc.models import factories


class MockObject(roleable.Roleable, Identifiable, db.Model):
  __tablename__ = "mock_table"


@ddt.ddt
class TestAccessControlRoleable(TestCase):
  """TestAccessControlList"""

  def setUp(self):
    super(TestAccessControlRoleable, self).setUp()
    with factories.single_commit():
      self.role = factories.AccessControlRoleFactory()
      self.person = factories.PersonFactory()

  @ddt.data(lambda self: [{
      "ac_role_id": self.role.id,
      "person": {
          "id": self.person.id
      }
  }], lambda self: [{
      "person": self.person,
      "ac_role": self.role
  }])
  def test_with_dict(self, acl_list):
    """Test access_control_list setter with a basic dict object
    This is the format the frontend uses"""
    obj = MockObject(access_control_list=acl_list(self))
    assert obj.access_control_list is not None
    acl = obj.access_control_list[0]
    assert acl is not None
    assert isinstance(acl, all_models.AccessControlList)
    assert acl.person.id == self.person.id
    assert acl.ac_role.id == self.role.id
    assert acl.object == obj

  def test_with_dict_objs_multiple(self):
    """Test access_control_list setter without ids"""
    person_1 = all_models.Person(name="Frodo", email="frodo@baggins.com")
    person_2 = all_models.Person(name="Bilbo", email="bilbo@baggins.com")
    role = all_models.AccessControlRole(name="Hobbit")
    obj = all_models.Control(title="Test Control", access_control_list=[{
        "person": person_1,
        "ac_role": self.role,
    }, {
        "person": person_2,
        "ac_role": role,
    }])
    db.session.commit()
    assert obj.access_control_list is not None
    assert len(obj.access_control_list) == 2
    assert obj.access_control_list[0].person == person_1
    assert obj.access_control_list[1].person == person_2
    num_acls = all_models.AccessControlList.query.filter(
        all_models.AccessControlList.object_id == obj.id,
        all_models.AccessControlList.object_type == "Control"
    ).count()
    assert num_acls == 2
