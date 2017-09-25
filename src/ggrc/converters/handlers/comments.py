# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handlers comment entries."""

from ggrc import db

from ggrc.converters import errors
from ggrc.converters.handlers.handlers import ColumnHandler
from ggrc.models import Comment
from ggrc.models import Relationship
from ggrc.models.comment import Commentable
from ggrc.login import get_current_user_id


class CommentColumnHandler(ColumnHandler):
  """ Handler for comments """

  COMMENTS_SEPARATOR = ";;"

  def parse_item(self):
    """Parse a list of comments to be mapped.

    Parse a semicolon separated list of comments

    Returns:
      list of commentst
    """
    if not isinstance(self.row_converter.obj, Commentable):
      self.add_error(errors.UNSUPPORTED_OPERATION_ERROR,
                     operation="Can't import comments for {}"
                     .format(self.row_converter.obj.__class__.__name__))
    comments = [comment for comment in
                self.raw_value.split(self.COMMENTS_SEPARATOR) if comment]
    if self.raw_value and not comments:
      self.add_warning(errors.WRONG_VALUE,
                       column_name=self.display_name)
    return comments

  def get_value(self):
    return ""

  def set_obj_attr(self):
    """ Create comments """
    if self.dry_run or not self.value:
      return
    current_obj = self.row_converter.obj
    for description in self.value:
      comment = Comment(description=description,
                        modified_by_id=get_current_user_id())
      db.session.add(comment)
      mapping = Relationship(source=current_obj, destination=comment)
      db.session.add(mapping)
