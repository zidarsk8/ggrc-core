# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from sqlalchemy import orm

from ggrc import db
from ggrc.models.mixins import Base


class ObjectFile(Base, db.Model):
  __tablename__ = 'object_files'

  file_id = db.Column(db.String, nullable=False)
  parent_folder_id = db.Column(db.String, nullable=True)
  fileable_id = db.Column(db.Integer, nullable=False)
  fileable_type = db.Column(db.String, nullable=False)

  @property
  def fileable_attr(self):
    return '{0}_fileable'.format(self.fileable_type)

  @property
  def fileable(self):
    return getattr(self, self.fileable_attr)

  @fileable.setter
  def fileable(self, value):
    self.fileable_id = value.id if value is not None else None
    self.fileable_type = value.__class__.__name__ if value is not None \
        else None
    return setattr(self, self.fileable_attr, value)

  _publish_attrs = [
      'file_id',
      'parent_folder_id',
      'fileable',
  ]

  @classmethod
  def eager_query(cls):
    query = super(ObjectFile, cls).eager_query()
    return query.options()

  def _display_name(self):
    return self.fileable.display_name + '<-> gdrive file' + self.file_id


class Fileable(object):

  @classmethod
  def late_init_fileable(cls):
    def make_object_files(cls):
      joinstr = 'and_(foreign(ObjectFile.fileable_id) == {type}.id, '\
          'foreign(ObjectFile.fileable_type) == "{type}")'
      joinstr = joinstr.format(type=cls.__name__)
      return db.relationship(
          'ObjectFile',
          primaryjoin=joinstr,
          backref='{0}_fileable'.format(cls.__name__),
          cascade='all, delete-orphan',
      )
    cls.object_files = make_object_files(cls)

  _publish_attrs = [
      'object_files',
  ]

  @classmethod
  def eager_query(cls):
    query = super(Fileable, cls).eager_query()
    return query.options(
        orm.subqueryload('object_files'))
