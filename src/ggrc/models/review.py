# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Review model."""
import datetime

import sqlalchemy as sa

from ggrc import db
from ggrc import builder
from ggrc.access_control import role
from ggrc.access_control import roleable
from ggrc.login import get_current_user
from ggrc.models import mixins, exceptions
from ggrc.models import utils as model_utils
from ggrc.models import reflection
from ggrc.models.mixins import issue_tracker
from ggrc.models.mixins import rest_handable
from ggrc.models.mixins import with_proposal_handable
from ggrc.models.mixins import with_mappimg_via_import_handable

from ggrc.models.relationship import Relatable
from ggrc.fulltext import mixin as ft_mixin

from ggrc.notifications import add_notification


class Reviewable(rest_handable.WithPutHandable,
                 rest_handable.WithRelationshipsHandable,
                 with_proposal_handable.WithProposalHandable,
                 with_mappimg_via_import_handable.WithMappingImportHandable):
  """Mixin to setup object as reviewable."""

  # REST properties
  _api_attrs = reflection.ApiAttributes(
      reflection.Attribute("review", create=False, update=False),
      reflection.Attribute("review_status", create=False, update=False),
      reflection.Attribute("review_issue_link", create=False, update=False),
  )

  _fulltext_attrs = ["review_status", "review_issue_link"]

  _aliases = {
      "review_status": {
          "display_name": "Review State",
          "mandatory": False
      }
  }

  @builder.simple_property
  def review_status(self):
    return self.review.status if self.review else Review.STATES.UNREVIEWED

  @builder.simple_property
  def review_issue_link(self):
    """Returns review issue link for reviewable object."""
    if not self.review:
      return None
    if not self.review.issuetracker_issue:
      return None
    notification_type = self.review.notification_type
    if notification_type != Review.NotificationTypes.ISSUE_TRACKER:
      return None
    return self.review.issuetracker_issue.issue_url

  @sa.ext.declarative.declared_attr
  def review(cls):  # pylint: disable=no-self-argument
    """Declare review relationship for reviewable object."""

    def join_function():
      return sa.and_(sa.orm.foreign(Review.reviewable_type) == cls.__name__,
                     sa.orm.foreign(Review.reviewable_id) == cls.id)

    return sa.orm.relationship(
        Review,
        primaryjoin=join_function,
        backref=Review.REVIEWABLE_TMPL.format(cls.__name__),
        uselist=False,
    )

  @classmethod
  def eager_query(cls):
    return super(Reviewable, cls).eager_query().options(
        sa.orm.joinedload("review")
    )

  def log_json(self):
    """Serialize to JSON"""
    out_json = super(Reviewable, self).log_json()
    out_json["review_status"] = self.review_status
    out_json["review"] = self.review
    out_json["review_issue_link"] = self.review_issue_link
    return out_json

  ATTRS_TO_IGNORE = {"review", "updated_at", "modified_by_id",
                     "slug", "_access_control_list"}

  def _update_status_on_attr(self):
    """Update review status when reviewable attrs are changed"""
    from ggrc.models import all_models
    if (self.review and
            self.review.status != all_models.Review.STATES.UNREVIEWED):
      changed = {a.key for a in db.inspect(self).attrs
                 if a.history.has_changes()}

      if changed - self.ATTRS_TO_IGNORE:
        self._set_review_status_unreviewed()

  def add_email_notification(self):
    """Add email notification of type STATUS_UNREVIEWED"""
    review_notif_type = self.review.notification_type
    if review_notif_type == Review.NotificationTypes.EMAIL_TYPE:
      add_notification(self.review,
                       Review.NotificationObjectTypes.STATUS_UNREVIEWED)

  def _update_status_on_mapping(self, counterparty):
    """Update review status on mapping to reviewable"""
    from ggrc.snapshotter.rules import Types
    from ggrc.models import all_models
    if self.review_status != all_models.Review.STATES.UNREVIEWED:
      if counterparty.type in Types.all:
        self._set_review_status_unreviewed()

  def _set_review_status_unreviewed(self):
    """Set review status -> unreviewed"""
    from ggrc.models import all_models
    if self.review:
      self.review.status = all_models.Review.STATES.UNREVIEWED
      self.add_email_notification()

  def handle_put(self):
    self._update_status_on_attr()

  def handle_relationship_post(self, counterparty):
    self._update_status_on_mapping(counterparty)

  def handle_relationship_delete(self, counterparty):
    self._update_status_on_mapping(counterparty)

  def handle_proposal_applied(self):
    self._set_review_status_unreviewed()

  def handle_mapping_via_import_created(self):
    self._set_review_status_unreviewed()


class Review(mixins.person_relation_factory("last_reviewed_by"),
             mixins.person_relation_factory("created_by"),
             mixins.datetime_mixin_factory("last_reviewed_at"),
             mixins.Stateful,
             rest_handable.WithPostHandable,
             rest_handable.WithPutHandable,
             roleable.Roleable,
             issue_tracker.IssueTracked,
             Relatable,
             mixins.base.ContextRBAC,
             mixins.Base,
             ft_mixin.Indexed,
             db.Model):
  """Review object"""
  # pylint: disable=too-few-public-methods
  __tablename__ = "reviews"

  REVIEWER_ROLE_NAME = "Reviewer"

  class STATES(object):
    """Review states container """
    REVIEWED = "Reviewed"
    UNREVIEWED = "Unreviewed"

  VALID_STATES = [STATES.UNREVIEWED, STATES.REVIEWED]

  class NotificationTypes(object):
    """Notification types container """
    EMAIL_TYPE = "email"
    ISSUE_TRACKER = "issue_tracker"

  class NotificationObjectTypes(object):
    """Review Notification Object types container """
    STATUS_UNREVIEWED = "review_status_unreviewed"
    REVIEW_CREATED = "review_request_created"

  reviewable_id = db.Column(db.Integer, nullable=False)
  reviewable_type = db.Column(db.String, nullable=False)

  REVIEWABLE_TMPL = "{}_reviewable"

  reviewable = model_utils.json_polymorphic_relationship_factory(
      Reviewable
  )(
      "reviewable_id", "reviewable_type", REVIEWABLE_TMPL
  )

  notification_type = db.Column(
      sa.types.Enum(NotificationTypes.EMAIL_TYPE,
                    NotificationTypes.ISSUE_TRACKER),
      nullable=False,
  )
  email_message = db.Column(db.Text, nullable=False, default=u"")

  _api_attrs = reflection.ApiAttributes(
      "notification_type",
      "email_message",
      reflection.Attribute("reviewable", update=False),
      reflection.Attribute("last_reviewed_by", create=False, update=False),
      reflection.Attribute("last_reviewed_at", create=False, update=False),
      "issuetracker_issue",
      "status",
  )

  _fulltext_attrs = [
      "reviewable_id",
      "reviewable_type",
  ]

  def validate_acl(self):
    """Reviewer is mandatory Role"""
    super(Review, self).validate_acl()
    review_global_roles = role.get_ac_roles_data_for("Review").values()
    mandatory_role_ids = {acr[0] for acr in review_global_roles if acr[3]}
    passed_acr_ids = {acl.ac_role_id for _, acl in self.access_control_list}
    missed_mandatory_roles = mandatory_role_ids - passed_acr_ids
    if missed_mandatory_roles:
      raise exceptions.ValidationError("{} roles are mandatory".format(
          ",".join(missed_mandatory_roles))
      )

  def handle_post(self):
    self._create_relationship()
    self._update_new_reviewed_by()
    if (self.notification_type == Review.NotificationTypes.EMAIL_TYPE and
            self.status == Review.STATES.UNREVIEWED):
      add_notification(self, Review.NotificationObjectTypes.REVIEW_CREATED)

  def handle_put(self):
    self._update_reviewed_by()

  def _create_relationship(self):
    """Create relationship for newly created review (used for ACL)"""
    from ggrc.models import all_models
    if self in db.session.new:
      db.session.add(
          all_models.Relationship(source=self.reviewable, destination=self)
      )

  def _update_new_reviewed_by(self):
    """When create new review with state REVIEWED set last_reviewed_by"""
    # pylint: disable=attribute-defined-outside-init
    from ggrc.models import all_models
    if self.status == all_models.Review.STATES.REVIEWED:
      self.last_reviewed_by = get_current_user()
      self.last_reviewed_at = datetime.datetime.utcnow()

  def _update_reviewed_by(self):
    """Update last_reviewed_by, last_reviewed_at"""
    # pylint: disable=attribute-defined-outside-init
    from ggrc.models import all_models
    if not db.inspect(self).attrs["status"].history.has_changes():
      return

    self.reviewable.updated_at = datetime.datetime.utcnow()

    if self.status == all_models.Review.STATES.REVIEWED:
      self.last_reviewed_by = self.modified_by
      self.last_reviewed_at = datetime.datetime.utcnow()
