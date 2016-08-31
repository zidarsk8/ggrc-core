# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handlers for special object mappings."""

from flask import current_app

from ggrc import models
from ggrc.login import get_current_user_id
from ggrc.converters.handlers import handlers


class RequestLinkHandler(handlers.ColumnHandler):

  def parse_item(self):
    documents = []
    for line in self.raw_value.splitlines():
      link, title = line.split(None, 1) if " " in line else (line, line)
      documents.append(models.Document(
          link=link,
          title=title,
          modified_by_id=get_current_user_id(),
          context=self.row_converter.obj.context,
      ))

    return documents

  def _get_link_str(self, documents):
    lines = []
    for document in documents:
      lines.append("{} {}".format(document.link, document.title))
    return "\n".join(lines)

  def set_obj_attr(self):
    self.value = self.parse_item()


class RequestEvidenceHandler(RequestLinkHandler):

  def get_value(self):
    return self._get_link_str(self.row_converter.obj.documents)

  def insert_object(self):
    if not self.value or self.row_converter.ignore:
      return

    new_link_map = {doc.link: doc for doc in self.value}
    old_link_map = {doc.link: doc for doc in self.row_converter.obj.documents}
    for new_link, new_doc in new_link_map.items():
      if new_link in old_link_map:
        old_link_map[new_link].title = new_doc.title
      else:
        self.row_converter.obj.documents.append(new_doc)

    for old_link, old_doc in old_link_map.items():
      if old_link not in new_link_map:
        self.row_converter.obj.documents.remove(old_doc)

  def set_value(self):
    """This should be ignored with second class attributes."""


class RequestUrlHandler(RequestLinkHandler):

  def get_value(self):
    documents = [doc for doc in self.row_converter.obj.related_objects()
                 if isinstance(doc, models.Document)]
    return self._get_link_str(documents)

  def insert_object(self):
    """Update request url values

    This function adds missing URLs and remove existing ones from requests.
    The existing URLs with new titles just change the title.
    """
    if not self.value or self.row_converter.ignore:
      return

    new_link_map = {doc.link: doc for doc in self.value}
    old_link_map = {doc.link: doc
                    for doc in self.row_converter.obj.related_objects()
                    if isinstance(doc, models.Document)}

    for new_link, new_doc in new_link_map.items():
      if new_link in old_link_map:
        old_link_map[new_link].title = new_doc.title
      else:
        models.Relationship(
            source=self.row_converter.obj,
            destination=new_doc,
        )

    for old_link, old_doc in old_link_map.items():
      if old_link not in new_link_map:
        if old_doc in self.row_converter.obj.related_destinations:
          self.row_converter.obj.related_destinations.remove(old_doc)
        elif old_doc in self.row_converter.obj.related_sources:
          self.row_converter.obj.related_sources.remove(old_doc)
        else:
          current_app.logger.warning("Invalid relationship state for request "
                                     "URLs.")

  def set_value(self):
    """This should be ignored with second class attributes."""
