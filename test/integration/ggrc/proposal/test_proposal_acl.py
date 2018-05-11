# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test for proposal api."""

import unittest

import ddt

from ggrc.models import all_models

from integration.ggrc import TestCase
from integration.ggrc.api_helper import Api
from integration.ggrc.models import factories


@ddt.ddt
@unittest.skip("Deprecated functionality: will be fixed in scope of GGRC-4991")
class TestACLPopulation(TestCase):
  """Test population permissions for controlproposals."""

  def setUp(self):
    super(TestACLPopulation, self).setUp()
    self.api = Api()
    self.client.get("/login")

  @ddt.data(
      {"read": 1, "update": 0},
      {"read": 0, "update": 1},
      {"read": 1, "update": 1},
      {"read": 0, "update": 0},
  )
  @ddt.unpack
  def test_proposal_acl_poulation(self, read, update):
    """Test proposal perms with read {read} and update {update}."""
    with factories.single_commit():
      control = factories.ControlFactory(title="1")
      role = factories.AccessControlRoleFactory(object_type=control.type,
                                                name="role",
                                                read=read,
                                                update=update)
      proposal = factories.ProposalFactory(instance=control,
                                           content={"field": "a"},
                                           agenda="agenda content")
      person = factories.PersonFactory()
    self.assertFalse(proposal.access_control_list)
    role_id = role.id
    control_id = control.id
    proposal_id = proposal.id
    control_content = control.log_json()
    control_content["access_control_list"] = [
        {"ac_role_id": role_id,
            "person": {"type": "Person", "id": person.id}}
    ]
    resp = self.api.put(control, {"control": control_content})
    self.assertEqual(200, resp.status_code)
    control = all_models.Control.query.get(control_id)
    proposal = all_models.Proposal.query.get(proposal_id)
    full_proposal_acls = all_models.AccessControlList.query.filter(
        all_models.AccessControlList.object_type == proposal.type,
        all_models.AccessControlList.object_id == proposal.id,
    ).all()
    self.assertEqual(int(read or update),
                     len(full_proposal_acls))
