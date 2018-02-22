# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test for proposal cav api."""

import ddt

from ggrc.models import all_models

from integration.ggrc.models import factories
from integration.ggrc.proposal.api import base


@ddt.ddt
class TestCADProposalsApi(base.BaseTestProposalApi):
  """Test for proposal cav api."""

  def test_change_cad(self):
    """Test create proposal with change CAVs."""
    with factories.single_commit():
      control = factories.ControlFactory(title="1")
      cad = factories.CustomAttributeDefinitionFactory(
          definition_type="control")
      factories.CustomAttributeValueFactory(
          custom_attribute=cad,
          attributable=control,
          attribute_value="123")
    control_id = control.id
    cad_id = cad.id
    data = control.log_json()
    del data["custom_attributes"]
    data["custom_attribute_values"][0]["attribute_value"] = "321"
    self.create_proposal(control,
                         full_instance_content=data,
                         agenda="update cav",
                         context=None)
    control = all_models.Control.query.get(control_id)
    self.assertEqual(1, len(control.proposals))
    self.assertIn("custom_attribute_values", control.proposals[0].content)
    self.assertEqual({unicode(cad_id): {"attribute_value": u"321",
                                        "attribute_object": None,
                                        "remove_cav": False}},
                     control.proposals[0].content["custom_attribute_values"])
    self.assertEqual(1, len(control.comments))

  @ddt.data(True, False)
  def test_apply_cad(self, remove_cav):
    """Test apply proposal with change CAVs."""
    with factories.single_commit():
      control = factories.ControlFactory(title="1")
      cad = factories.CustomAttributeDefinitionFactory(
          definition_type="control")
    control_id = control.id
    proposal = factories.ProposalFactory(
        instance=control,
        content={
            "custom_attribute_values": {
                cad.id: {
                    "attribute_value": "321",
                    "attribute_object": None,
                    "remove_cav": remove_cav,
                },
            },
        },
        agenda="agenda content")
    with self.number_obj_revisions_for(control):
      self.apply_proposal(proposal)
    control = all_models.Control.query.get(control_id)
    self.assertEqual(
        "321",
        control.custom_attribute_values[0].attribute_value)

  @ddt.data(True, False)
  def test_apply_mapping_cad(self, remove_cav):
    """Test apply mapping CAVs proposal with remove_cav is {0}."""
    with factories.single_commit():
      control = factories.ControlFactory(title="1")
      cad = factories.CustomAttributeDefinitionFactory(
          definition_type="control",
          attribute_type="Map:Person"
      )
      person = factories.PersonFactory()
      cav = factories.CustomAttributeValueFactory(
          custom_attribute=cad,
          attributable=control,
          attribute_object_id=person.id,
          attribute_value="Person",
      )
    self.assertEqual(person,
                     control.custom_attribute_values[0].attribute_object)
    control_id = control.id
    proposal = factories.ProposalFactory(
        instance=control,
        content={
            "custom_attribute_values": {
                cad.id: {
                    "attribute_value": "Person",
                    "attribute_object": None,
                    "remove_cav": remove_cav,
                },
            },
        },
        agenda="agenda content")
    with self.number_obj_revisions_for(control):
      self.apply_proposal(proposal)
    control = all_models.Control.query.get(control_id)
    if remove_cav:
      self.assertFalse(control.custom_attribute_values)
    else:
      cav = control.custom_attribute_values[0]
      self.assertEqual("Person", cav.attribute_value)
      self.assertIsNone(cav.attribute_object_id)

  def test_change_cad_oldstile(self):
    """Test create CAVs proposal in old style."""
    with factories.single_commit():
      control = factories.ControlFactory(title="1")
      cad = factories.CustomAttributeDefinitionFactory(
          definition_type="control")
      factories.CustomAttributeValueFactory(
          custom_attribute=cad,
          attributable=control,
          attribute_value="123")
    control_id = control.id
    cad_id = cad.id
    data = control.log_json()
    data["custom_attributes"] = {cad.id: "321"}
    self.create_proposal(control,
                         full_instance_content=data,
                         agenda="update cav",
                         context=None)
    control = all_models.Control.query.get(control_id)
    self.assertEqual(1, len(control.proposals))
    self.assertIn("custom_attribute_values", control.proposals[0].content)
    self.assertEqual({unicode(cad_id): {"attribute_value": u"321",
                                        "attribute_object": None,
                                        "remove_cav": True}},
                     control.proposals[0].content["custom_attribute_values"])
    self.assertEqual(1, len(control.comments))
