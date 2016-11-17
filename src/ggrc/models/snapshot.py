# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for Snapshot object"""

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import orm
from sqlalchemy import event
from sqlalchemy.orm.session import Session

from ggrc import db
from ggrc.models import mixins
from ggrc.models import reflection
from ggrc.models import relationship
from ggrc.models.deferred import deferred
from ggrc.models.computed_property import computed_property


def get_latest_revision_id(snapshot):
  """Retrieve last revision saved for snapshots

  Args:
    snapshot: Instance of models.Snapshot
  Returns:
    ID of the latest revision or None otherwise
  """
  from ggrc.snapshotter.helpers import get_revisions
  from ggrc.snapshotter.datastructures import Pair
  pair = Pair.from_snapshot(snapshot)
  revisions = get_revisions({pair}, revisions=set())
  if pair in revisions and revisions[pair]:
    return revisions[pair]


class Snapshot(relationship.Relatable, mixins.Base, db.Model):
  """Snapshot object that holds a join of parent object, revision, child object
  and parent object's context.

  Conceptual model is that we have a parent snapshotable object (e.g. Audit)
  which will not create relationships to objects with automapper at the time of
  creation but will instead create snapshots of those objects based on the
  latest revision of the object at the time of create / update of the object.
  Objects that were supposed to be mapped are called child objects.
  """
  __tablename__ = "snapshots"

  _publish_attrs = [
      "parent",
      "child_id",
      "child_type",
      "revision",
      "revision_id",
      reflection.PublishOnly("revision_content"),
  ]

  _update_attrs = [
      "parent",
      "child_id",
      "child_type",
      "update_revision"
  ]

  _include_links = [
      "revision"
  ]

  parent_id = deferred(db.Column(db.Integer, nullable=False), "Snapshot")
  parent_type = deferred(db.Column(db.String, nullable=False), "Snapshot")

  # Child ID and child type are data denormalisations - we could easily get
  # them from revision.content, but since that is a JSON field it will be
  # easier for development to just denormalise on write and not worry
  # about it.
  child_id = deferred(db.Column(db.Integer, nullable=False), "Snapshot")
  child_type = deferred(db.Column(db.String, nullable=False), "Snapshot")

  revision_id = deferred(db.Column(
      db.Integer,
      db.ForeignKey("revisions.id"),
      nullable=False
  ), "Snapshot")
  revision = db.relationship(
      "Revision",
  )

  @classmethod
  def eager_query(cls):
    query = super(Snapshot, cls).eager_query()
    return cls.eager_inclusions(query, Snapshot._include_links).options(
        orm.subqueryload('revision'),
    )

  @hybrid_property
  def update_revision(self):
    return self.revision_id

  @update_revision.setter
  def update_revision(self, value):
    self._update_revision = value
    if value == "latest":
      latest_revision_id = get_latest_revision_id(self)
      if latest_revision_id:
        self.revision_id = latest_revision_id

  @computed_property
  def revision_content(self):
    return self.revision.content

  @property
  def parent_attr(self):
    return '{0}_parent'.format(self.parent_type)

  @property
  def parent(self):
    return getattr(self, self.parent_attr)

  @parent.setter
  def parent(self, value):
    self.parent_id = getattr(value, 'id', None)
    self.parent_type = getattr(value, 'type', None)
    return setattr(self, self.parent_attr, value)

  @staticmethod
  def _extra_table_args(_):
    return (
        db.UniqueConstraint(
            "parent_type", "parent_id",
            "child_type", "child_id"),
        db.Index("ix_snapshots_parent", "parent_type", "parent_id"),
        db.Index("ix_snapshots_child", "child_type", "child_id"),
    )

  @classmethod
  def handle_post_flush(cls, session, flush_context, instances):
    objects = [
        o for o in session.new
        if isinstance(o, cls) and getattr(o, "_update_revision", "") == "new"
    ]
    if not objects:
      return
    cls._set_revisions(objects)
    cls._ensure_relationships(objects)

  @classmethod
  def _ensure_relationships(cls, objects):
    pass

  @classmethod
  def _set_revisions(cls, objects):
    pass


class Snapshotable(object):
  """Provide `snapshotted_objects` on for parent objects."""

  _publish_attrs = [
      "snapshotted_objects",
  ]

  @declared_attr
  def snapshotted_objects(cls):  # pylint: disable=no-self-argument
    """Return all snapshotted objects"""
    joinstr = "and_(remote(Snapshot.parent_id) == {type}.id, " \
              "remote(Snapshot.parent_type) == '{type}')"
    joinstr = joinstr.format(type=cls.__name__)
    return db.relationship(
        lambda: Snapshot,
        primaryjoin=joinstr,
        foreign_keys='Snapshot.parent_id,Snapshot.parent_type,',
        backref='{0}_parent'.format(cls.__name__),
        cascade='all, delete-orphan')

  @classmethod
  def eager_query(cls):
    query = super(Snapshotable, cls).eager_query()
    return query.options(
        orm.subqueryload("snapshotted_objects").undefer_group(
            "Snapshot_complete"
        ),
    )


event.listen(Session, 'before_flush', Snapshot.handle_post_flush)
