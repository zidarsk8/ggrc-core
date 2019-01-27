# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Services for create and manipulate Proposal objects via UI."""
from lib import factory, base
from lib.constants import objects
from lib.page import proposal_digest


class ProposalDigestService(base.WithBrowser):
  """Class for Proposal Digest business layer's services objects."""

  def open_proposal_digest(self):
    """Open proposal digest."""
    proposal_digest.ProposalDigest(self._driver).open_proposal_digest()

  def opened_obj(self, obj, proposal_email):
    """Build obj from page after clicking on the Open btn in the proposal
    notification email."""
    proposal_digest.ProposalDigest(
        self._driver).click_proposal_email_open_btn(proposal_email)
    obj_name = objects.get_plural(obj.type)
    service_cls = factory.get_cls_webui_service(obj_name)(self._driver)
    return service_cls.build_obj_from_page()
