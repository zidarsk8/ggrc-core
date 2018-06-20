# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handlers evidence entries."""

from logging import getLogger
from ggrc import db
from ggrc.models import all_models
from ggrc.converters import errors
from ggrc.converters.handlers import handlers
from ggrc.login import get_current_user_id


logger = getLogger(__name__)


class EvidenceUrlHandler(handlers.ColumnHandler):
  """Handler for Evidence URL field on evidence imports."""

  KIND = all_models.Evidence.URL

  def _get_old_map(self):
    return {d.link: d for d in self.row_converter.obj.evidences_url}

  def get_value(self):
    """Generate a new line separated string for all document links.

    Returns:
      string containing all URLs
    """
    return "\n".join(doc.link for doc in self.row_converter.obj.evidences_url)

  def build_evidence(self, link, user_id):
    """Build evidence object"""
    evidence = all_models.Evidence(
        link=link,
        title=link,
        modified_by_id=user_id,
        context=self.row_converter.obj.context,
        kind=self.KIND,
    )
    evidence.add_admin_role()
    return evidence

  def parse_item(self):
    """Parse evidence link lines.

    Returns:
      list of evidences for all URLs and evidences.
    """
    evidences = []
    if self.raw_value:
      seen_links = set()
      duplicate_links = set()
      user_id = get_current_user_id()

      for line in self.raw_value.splitlines():
        link = line.strip()
        if not link:
          continue

        if link not in seen_links:
          seen_links.add(link)
          evidences.append(self.build_evidence(link, user_id))
        else:
          duplicate_links.add(link)

      if duplicate_links:
        # NOTE: We rely on the fact that links in duplicate_links are all
        # instances of unicode (if that assumption breaks,
        # unicode encode/decode errors can occur for non-ascii link values)
        self.add_warning(errors.DUPLICATE_IN_MULTI_VALUE,
                         column_name=self.display_name,
                         duplicates=u", ".join(sorted(duplicate_links)))

    return evidences

  def set_obj_attr(self):
    self.value = self.parse_item()

  def set_value(self):
    """This should be ignored with second class attributes."""

  def insert_object(self):
    """Update document URL values

    This function adds missing URLs and remove existing ones from Documents.
    The existing URLs with new titles just change the title.
    """
    if self.row_converter.ignore:
      return
    new_link_map = {d.link: d for d in self.value}
    old_link_map = self._get_old_map()

    for new_link, new_evidence in new_link_map.iteritems():
      if new_link not in old_link_map:
        all_models.Relationship(source=self.row_converter.obj,
                                destination=new_evidence)
      else:
        db.session.expunge(new_evidence)

    for old_link, old_evidence in old_link_map.iteritems():
      if old_link in new_link_map:
        continue
      if old_evidence.related_destinations:
        old_evidence.related_destinations.pop()
      elif old_evidence.related_sources:
        old_evidence.related_sources.pop()
      else:
        logger.warning("Invalid relationship state for document URLs.")


class EvidenceFileHandler(handlers.ColumnHandler):
  """Handler for evidence of type file on evidence imports."""

  def set_obj_attr(self):
    """Is not allowed to import evidence of type File

    if file already mapped to parent we ignore it and not show warning
    """
    if self.raw_value:
      parent = self.row_converter.obj
      existing_evid_file_links = {evid.link for evid in parent.evidences_file}
      for line in self.raw_value.splitlines():
        link, _ = self._parse_line(line)
        if link not in existing_evid_file_links:
          self.add_warning(errors.DISALLOW_EVIDENCE_FILE)

  def insert_object(self):
    """Import not allowed"""
    pass

  @staticmethod
  def _parse_line(line):
    """Parse a single line and return link and title.

    Args:
      line: string containing a single line from a cell.

    Returns:
      tuple containing a link and a title.
    """
    parts = line.strip().split()
    return parts[0], parts[0] if len(parts) == 1 else " ".join(parts[1:])

  def get_value(self):
    """Generate a new line separated string for all document links.

    Returns:
      string containing all evidence URLs and titles.
    """
    return u"\n".join(u"{} {}".format(d.link, d.title) for d in
                      self.row_converter.obj.evidences_file)
