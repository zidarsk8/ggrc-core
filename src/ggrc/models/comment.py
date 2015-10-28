# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

from ggrc import db
from ggrc.models.mixins import Base, Described
from ggrc.models.object_document import Documentable
from sqlalchemy.ext.declarative import declared_attr


class Comment(Described, Documentable, Base, db.Model):
  __tablename__ = "comments"

  commentable_id = db.Column(db.Integer, nullable=False)
  commentable_type = db.Column(db.String, nullable=False)

  @property
  def commentable_attr(self):
    return '{0}_commentable'.format(self.commentable_type)

  @property
  def commentable(self):
    return getattr(self, self.commentable_type)

  @commentable.setter
  def commentable(self, value):
    self.commentable_id = value.id if value is not None else None
    self.commentable_type = \
        value.__class__.__name__ if value is not None else None
    return setattr(self, self.commentable_attr, value)

  _publish_attrs = [
      "commentable"
  ]


class Commentable(object):

  @declared_attr
  def comments(cls):
    joinstr = 'and_(remote(Comment.commentable_id) == {type}.id, '\
        'remote(Comment.commentable_type) == "{type}")'
    joinstr = joinstr.format(type=cls.__name__)
    return db.relationship(
        'Comment',
        primaryjoin=joinstr,
        foreign_keys='Comment.commentable_id',
        backref='{0}_commentable'.format(cls.__name__),
        cascade='all, delete-orphan')

  _publish_attrs = [
      "comments"
  ]
