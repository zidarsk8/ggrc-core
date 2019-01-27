# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Proposals digest."""

from lib import base, environment
from lib.entities import entity
from lib.utils import selenium_utils


class ProposalDigest(base.WithBrowser):
  """Proposals digest page."""
  def __init__(self, driver=None):
    super(ProposalDigest, self).__init__(driver)
    self.proposal_digest_url = (environment.app_url +
                                "_notifications/show_fast_digest")
    self._elements = self._browser.elements(
        xpath="//title/following-sibling::div/div"
              "[contains(., 'proposed changes')]")

  def open_proposal_digest(self):
    """Open page with proposal emails."""
    selenium_utils.open_url(self.proposal_digest_url)

  def get_proposal_emails(self):
    """Get all proposal notification emails."""
    return [ProposalDigestItem(element).get_proposal_email() for element in
            self._elements]

  def click_proposal_email_open_btn(self, proposal_email):
    """Click on the proposal email open button."""
    proposal_emails = self.get_proposal_emails()
    index = proposal_emails.index(proposal_email)
    ProposalDigestItem(self._elements[index]).open_btn_click()
    selenium_utils.wait_for_js_to_load(self._driver)


class ProposalDigestItem(object):
  """Proposal notification email."""
  def __init__(self, root_element):
    self._root_element = root_element

  def get_proposal_email(self):
    """Get proposal email."""
    return entity.ProposalEmailUI(
        recipient_email=self.get_recipient_email(),
        author=self.get_proposal_author(),
        obj_type=self.get_proposal_obj_type(),
        changes=self.get_changes(),
        comment=self.get_comment()
    )

  def get_recipient_email(self):
    """Get email recipient."""
    return self._root_element.parent().previous_sibling(
        tag_name="h1").text.replace("email to ", "")

  def get_proposal_author(self):
    """Get proposal author."""
    return self._root_element.h1().text.split(" proposed ")[0]

  def get_proposal_obj_type(self):
    """Get proposal obj type."""
    return self._root_element.h1().text.split(" to ")[1].split(":")[0]

  def get_changes(self):
    """Get proposal changes need view."""
    changes_list = []
    for row in self._root_element.tbody().trs():
      row_element_texts = [element.text for element in row.tds()]
      change = {"obj_attr_type": row_element_texts[0],
                "proposed_value": row_element_texts[1]}
      changes_list.append(change)
    return changes_list

  def get_comment(self):
    """Get proposal comment."""
    comment_str = "".join(
        el.text for el in self._root_element.table().previous_siblings(
            tag_name="p"))
    return None if comment_str == "" else comment_str

  def open_btn_click(self):
    """Click on the open button in email."""
    self._root_element.link().click()
