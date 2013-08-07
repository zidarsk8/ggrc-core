# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from .mixins import deferred, Base
from .reflection import PublishOnly

class Person(Base, db.Model):
  __tablename__ = 'people'

  email = deferred(db.Column(db.String), 'Person')
  name = deferred(db.Column(db.String), 'Person')
  language_id = deferred(db.Column(db.Integer), 'Person')
  company = deferred(db.Column(db.String), 'Person')

  object_people = db.relationship(
      'ObjectPerson', backref='person', cascade='all, delete-orphan')
  language = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Person.language_id) == Option.id, '\
                       'Option.role == "person_language")',
      uselist=False,
      )

  _publish_attrs = [
      'company',
      'email',
      'language',
      'name',
      PublishOnly('object_people'),
      ]

  # Methods required by Flask-Login
  def is_authenticated(self):
    return True

  def is_active(self):
    return True #self.active

  def is_anonymous(self):
    return False

  def get_id(self):
    return unicode(self.id)

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Person, cls).eager_query()
    return query.options(
        orm.joinedload('language'),
        orm.subqueryload('object_people'))

  def _display_name(self):
    return self.email
