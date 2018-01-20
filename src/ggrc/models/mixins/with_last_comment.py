# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Contains WithLastComment mixin.

This defines logic to get fields of the last Comment over all
Comments of object.
"""

from ggrc.fulltext import attributes
from ggrc.builder import simple_property
from ggrc.models import reflection
from ggrc.models.mixins import attributable


class WithLastComment(attributable.Attributable):
  """Defines logic to get last comment for object."""
  # pylint: disable=too-few-public-methods

  _api_attrs = reflection.ApiAttributes(
      reflection.Attribute("last_comment", create=False, update=False),
      reflection.Attribute("last_comment_id", create=False, update=False),
  )

  _aliases = {
      "last_comment": {
          "display_name": "Last Comment",
          "view_only": True,
      },
  }

  _fulltext_attrs = [attributes.FullTextAttr("last_comment", "last_comment")]

  @simple_property
  def last_comment_ca(self):
    return self.attribute_objs.get("last_comment")

  @simple_property
  def last_comment(self):
    return self.last_comment_ca.value_string if self.last_comment_ca else None

  @simple_property
  def last_comment_id(self):
    return self.last_comment_ca.source_id if self.last_comment_ca else None
