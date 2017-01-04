# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handlers document entries."""

from logging import getLogger

from ggrc import db
from ggrc import models
from ggrc.converters import errors
from ggrc.converters.handlers import handlers
from ggrc.login import get_current_user_id


# pylint: disable=invalid-name
logger = getLogger(__name__)


class DocumentLinkHandler(handlers.ColumnHandler):
  """Base class for document documents handlers."""

  def _parse_line(self, line):
    """Parse a single line and return link and title.

    Args:
      line: string containing a single line from a cell.

    Returns:
      tuple containing a link and a title.
    """
    # pylint: disable=no-self-use
    line = line.strip()
    return line, line

  def parse_item(self, has_title=False):
    """Parse document link lines.

    Returns:
      list of documents for all URLs and evidences.
    """
    documents = []
    user_id = get_current_user_id()
    for line in self.raw_value.splitlines():
      link, title = self._parse_line(line)
      if not (link and title):
        return []
      documents.append(models.Document(
          link=link,
          title=title,
          modified_by_id=user_id,
          context=self.row_converter.obj.context,
      ))

    return documents

  def set_obj_attr(self):
    self.value = self.parse_item()


class DocumentEvidenceHandler(DocumentLinkHandler):
  """Handler for evidence field on document imports."""

  def _parse_line(self, line):
    """Parse a single line and return link and title.

    Args:
      line: string containing a single line from a cell.

    Returns:
      tuple containing a link and a title.
    """
    # pylint: disable=no-self-use
    parts = line.strip().split()
    if len(parts) == 1:
      return parts[0], parts[0]

    return parts[0], " ".join(parts[1:])

  def get_value(self):
    """Generate a new line separated string for all document links.

    Returns:
      string containing all evidence URLs and titles.
    """
    return u"\n".join(
        u"{} {}".format(document.link, document.title)
        for document in self.row_converter.obj.documents
    )

  def insert_object(self):
    """Update document evidence values.

    This function adds missing evidence and remove existing ones from
    Documents. The existing evidence with new titles just change the title.
    """
    if not self.value or self.row_converter.ignore:
      return

    new_link_map = {doc.link: doc for doc in self.value}
    old_link_map = {doc.link: doc for doc in self.row_converter.obj.documents}
    for new_link, new_doc in new_link_map.iteritems():
      if new_link in old_link_map:
        old_link_map[new_link].title = new_doc.title
      else:
        self.row_converter.obj.documents.append(new_doc)

    for old_link, old_doc in old_link_map.iteritems():
      if old_link not in new_link_map:
        db.session.delete(old_doc.object_documents[0])

  def set_value(self):
    """This should be ignored with second class attributes."""


class DocumentUrlHandler(DocumentLinkHandler):
  """Handler for URL field on document imports."""

  def _parse_line(self, line):
    """Parse a single line and return link and title.

    Args:
      line: string containing a single line from a cell.

    Returns:
      tuple containing a link and a title.
    """
    line = line.strip()
    if len(line.split()) > 1:
      self.add_warning(errors.WRONG_VALUE, column_name=self.display_name)
      return None, None
    return line, line

  def get_value(self):
    """Generate a new line separated string for all document links.

    Returns:
      string containing all URLs
    """
    return "\n".join(
        doc.link
        for doc in self.row_converter.obj.related_objects()
        if isinstance(doc, models.Document)
    )

  def insert_object(self):
    """Update document URL values

    This function adds missing URLs and remove existing ones from Documents.
    The existing URLs with new titles just change the title.
    """
    if not self.value or self.row_converter.ignore:
      return

    new_link_map = {doc.link: doc for doc in self.value}
    old_link_map = {doc.link: doc
                    for doc in self.row_converter.obj.related_objects()
                    if isinstance(doc, models.Document)}

    for new_link, new_doc in new_link_map.iteritems():
      if new_link in old_link_map:
        old_link_map[new_link].title = new_doc.title
      else:
        models.Relationship(
            source=self.row_converter.obj,
            destination=new_doc,
        )

    for old_link, old_doc in old_link_map.iteritems():
      if old_link not in new_link_map:
        if old_doc.related_destinations:
          old_doc.related_destinations.pop()
        elif old_doc.related_sources:
          old_doc.related_sources.pop()
        else:
          logger.warning("Invalid relationship state for document URLs.")

  def set_value(self):
    """This should be ignored with second class attributes."""
