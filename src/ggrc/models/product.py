# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc import db
from sqlalchemy.orm import validates
from .mixins import deferred, BusinessObject, Timeboxed, CustomAttributable
from .object_document import Documentable
from .object_owner import Ownable
from .object_person import Personable
from .option import Option
from .relationship import Relatable
from .utils import validate_option
from .track_object_state import HasObjectState, track_state_for_class


class Product(HasObjectState, CustomAttributable, Documentable, Personable,
              Relatable, Timeboxed, Ownable, BusinessObject, db.Model):
  __tablename__ = 'products'

  kind_id = deferred(db.Column(db.Integer), 'Product')
  version = deferred(db.Column(db.String), 'Product')

  kind = db.relationship(
      'Option',
      primaryjoin='and_(foreign(Product.kind_id) == Option.id, '\
                       'Option.role == "product_type")',
      uselist=False,
  )

  _publish_attrs = [
      'kind',
      'version',
  ]
  _sanitize_html = ['version',]
  _aliases = {
    "url": "Product URL",
    "kind": {
      "display_name": "Kind/Type",
      "filter_by": "_filter_by_kind",
    },
  }

  @validates('kind')
  def validate_product_options(self, key, option):
    return validate_option(
        self.__class__.__name__, key, option, 'product_type')

  @classmethod
  def _filter_by_kind(cls, predicate):
    return Option.query.filter(
        (Option.id == cls.kind_id) & predicate(Option.title)
    ).exists()

  @classmethod
  def eager_query(cls):
    from sqlalchemy import orm

    query = super(Product, cls).eager_query()
    return query.options(orm.joinedload('kind'))

track_state_for_class(Product)
