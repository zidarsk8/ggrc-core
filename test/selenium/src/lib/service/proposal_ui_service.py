# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Services for create and manipulate Proposal objects via UI."""
from lib import factory, base
from lib.constants import objects
from lib.entities import entities_factory
from lib.page.widget import object_modal


class ProposalsService(base.WithBrowser):
  """Class for Proposals business layer's services objects."""

  def create_proposal(self, obj):
    """Create a proposal for an obj."""
    obj_info_page = factory.get_cls_webui_service(objects.get_plural(
        obj.type))(self._driver).open_info_page_of_obj(obj)
    obj_info_page.click_propose_changes()
    proposal_factory = entities_factory.ProposalsFactory()
    proposal = proposal_factory.create()
    proposed_description = proposal_factory.generate_string("Proposal")
    proposal_modal = object_modal.BaseObjectModal(self._driver)
    proposal_modal.set_description(proposed_description)
    proposal_modal.click_propose()
    proposal.changes = [{"obj_attr_type": "Description",
                         "cur_value": obj.description,
                         "proposed_value": proposed_description}]
    return proposal

  def open_obj_change_proposals_tab(self, obj):
    """Open change proposals tab of an obj."""
    obj_info_page = factory.get_cls_webui_service(objects.get_plural(
        obj.type))(self._driver).open_info_page_of_obj(obj)
    return obj_info_page.related_proposals()

  def get_related_proposals(self, obj):
    """Get related proposals."""
    return self.open_obj_change_proposals_tab(obj).get_proposals()

  def is_proposal_apply_btn_exist(self, obj, proposal):
    """Check if proposal apply btn exists for an obj."""
    return self.open_obj_change_proposals_tab(obj).has_apply_btn(proposal)
