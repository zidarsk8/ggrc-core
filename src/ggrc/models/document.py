# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module containing Document model."""

from sqlalchemy import orm
from sqlalchemy import func, case
from sqlalchemy.ext.hybrid import hybrid_property

from ggrc import db
from ggrc.access_control.roleable import Roleable
from ggrc.fulltext.mixin import Indexed
from ggrc.models.deferred import deferred
from ggrc.models.mixins import Base
from ggrc.models.relationship import Relatable
from ggrc.models import exceptions
from ggrc.models import reflection
from ggrc.models import mixins


class Document(Roleable, Relatable, Base, mixins.Titled, Indexed, db.Model):
  """Audit model."""
  __tablename__ = 'documents'

  _title_uniqueness = False

  link = deferred(db.Column(db.String), 'Document')
  description = deferred(db.Column(db.Text, nullable=False, default=u""),
                         'Document')

  URL = "URL"
  ATTACHMENT = "EVIDENCE"
  REFERENCE_URL = "REFERENCE_URL"
  VALID_DOCUMENT_TYPES = [URL, ATTACHMENT, REFERENCE_URL]
  document_type = deferred(db.Column(db.Enum(*VALID_DOCUMENT_TYPES),
                                     default=URL,
                                     nullable=False),
                           'Document')

  _fulltext_attrs = [
      'title',
      'link',
      'description',
      "document_type",
  ]

  _api_attrs = reflection.ApiAttributes(
      'title',
      'link',
      'description',
      "document_type",
  )

  _sanitize_html = [
      'title',
      'description',
  ]

  _aliases = {
      'title': "Title",
      'link': "Link",
      'description': "description",
  }

  @orm.validates('document_type')
  def validate_document_type(self, key, document_type):
    """Returns correct option, otherwise rises an error"""
    if document_type is None:
      document_type = self.URL
    if document_type not in self.VALID_DOCUMENT_TYPES:
      raise exceptions.ValidationError(
          "Invalid value for attribute {attr}. "
          "Expected options are `{url}`, `{attachment}`, `{reference_url}`".
          format(
              attr=key,
              url=self.URL,
              attachment=self.ATTACHMENT,
              reference_url=self.REFERENCE_URL
          )
      )
    return document_type

  @classmethod
  def indexed_query(cls):
    return super(Document, cls).indexed_query().options(
        orm.Load(cls).undefer_group(
            "Document_complete",
        ),
    )

  @hybrid_property
  def slug(self):
    if self.document_type in (self.URL, self.REFERENCE_URL):
      return self.link
    return u"{} {}".format(self.link, self.title)

  # pylint: disable=no-self-argument
  @slug.expression
  def slug(cls):
    return case([(cls.document_type == cls.ATTACHMENT,
                 func.concat(cls.link, ' ', cls.title))],
                else_=cls.link)

  def log_json(self):
    tmp = super(Document, self).log_json()
    tmp['type'] = "Document"
    return tmp
