# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handlers for special object mappings."""

from flask import current_app

from ggrc import models
from ggrc.login import get_current_user_id
from ggrc.converters import errors
from ggrc.converters import get_importables
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

  def set_obj_attr(self):
    self.value = self.parse_item()


class RequestEvidenceHandler(RequestLinkHandler):

  def get_value(self):
    lines = []
    for document in self.row_converter.obj.documents:
      lines.append("{} {}".format(document.link, document.title))
    return "\n".join(lines)


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
    pass

  def insert_object(self):
    pass

  def set_value(self):
    """This should be ignored with second class attributes."""

