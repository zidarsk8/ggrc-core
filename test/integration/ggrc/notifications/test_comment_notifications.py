# -*- coding: utf-8 -*-

# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for notifications for models with assignable mixin."""

from datetime import datetime

import ddt
from freezegun import freeze_time
from mock import patch
from sqlalchemy import and_

from ggrc import db
from ggrc.access_control.role import get_custom_roles_for
from ggrc.models import Assessment, all_models
from ggrc.models import Notification
from ggrc.models import NotificationType
from ggrc.models import Revision
from ggrc.notifications import common
from integration.ggrc import TestCase
from integration.ggrc import generator
from integration.ggrc.models import factories


@ddt.ddt
class TestCommentNotification(TestCase):

  """Test notification on assessment comments."""

  def setUp(self):
    super(TestCommentNotification, self).setUp()
    self.client.get("/login")
    self._fix_notification_init()
    self.generator = generator.ObjectGenerator()

  def _fix_notification_init(self):
    """Fix Notification object init function.

    This is a fix needed for correct created_at field when using freezgun. By
    default the created_at field is left empty and filed by database, which
    uses system time and not the fake date set by freezugun plugin. This fix
    makes sure that object created in feeze_time block has all dates set with
    the correct date and time.
    """

    def init_decorator(init):
      """Wrapper for Notification init function."""

      def new_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        if hasattr(self, "created_at"):
          self.created_at = datetime.now()
      return new_init

    Notification.__init__ = init_decorator(Notification.__init__)

  @classmethod
  def _get_notifications(cls, sent=False, notif_type=None):
    """Get a notification query.

    Args:
      sent (boolean): flag to filter out only notifications that have been
        sent.
      notif_type (string): name of the notification type.

    Returns:
      sqlalchemy query for selected notifications.
    """
    if sent:
      notif_filter = Notification.sent_at.isnot(None)
    else:
      notif_filter = Notification.sent_at.is_(None)

    if notif_type:
      notif_filter = and_(notif_filter, NotificationType.name == notif_type)

    return db.session.query(Notification).join(NotificationType).filter(
        notif_filter
    )

  @patch("ggrc.notifications.common.send_email")
  def test_notification_entries(self, _):
    """Test setting notification entries for assessment comments.

    Check if the correct notification entries are created when a comment gets
    posted.
    """

    factories.AuditFactory(slug="Audit")
    self.import_file("assessment_template_no_warnings.csv")
    self.import_file("assessment_with_templates.csv")
    asmt1 = Assessment.query.filter_by(slug="A 1").first()
    self.generator.generate_comment(
        asmt1, "Verifiers", "some comment", send_notification="true")

    notifications = self._get_notifications(notif_type="comment_created").all()
    self.assertEqual(len(notifications), 1,
                     "Missing comment notification entry.")
    notif = notifications[0]
    revisions = Revision.query.filter_by(resource_type='Notification',
                                         resource_id=notif.id).count()
    self.assertEqual(revisions, 1)

    self.client.get("/_notifications/send_daily_digest")

    notifications = self._get_notifications(notif_type="comment_created").all()
    self.assertEqual(len(notifications), 0,
                     "Found a comment notification that was not sent.")

  @patch("ggrc.notifications.common.send_email")
  def test_grouping_comments(self, _):
    """Test that comments are grouped by parent object in daily digest data."""

    factories.AuditFactory(slug="Audit")
    self.import_file("assessment_template_no_warnings.csv")
    self.import_file("assessment_with_templates.csv")
    asmt1 = Assessment.query.filter_by(slug="A 1").first()
    asmt4 = Assessment.query.filter_by(slug="A 4").first()
    asmt6 = Assessment.query.filter_by(slug="A 6").first()

    asmt_ids = (asmt1.id, asmt4.id, asmt6.id)

    self.generator.generate_comment(
        asmt1, "Verifiers", "comment X on asmt " + str(asmt1.id),
        send_notification="true")
    self.generator.generate_comment(
        asmt6, "Verifiers", "comment A on asmt " + str(asmt6.id),
        send_notification="true")
    self.generator.generate_comment(
        asmt4, "Verifiers", "comment FOO on asmt " + str(asmt4.id),
        send_notification="true")
    self.generator.generate_comment(
        asmt4, "Verifiers", "comment BAR on asmt " + str(asmt4.id),
        send_notification="true")
    self.generator.generate_comment(
        asmt1, "Verifiers", "comment Y on asmt " + str(asmt1.id),
        send_notification="true")

    _, notif_data = common.get_daily_notifications()

    assignee_notifs = notif_data.get("user@example.com", {})
    common.sort_comments(assignee_notifs)
    comment_notifs = assignee_notifs.get("comment_created", {})
    self.assertEqual(len(comment_notifs), 3)  # for 3 different Assessments

    # for each group of comment notifications, check that it contains comments
    # for that particular Assessment
    for parent_obj_key, comments_info in comment_notifs.iteritems():
      self.assertIn(parent_obj_key.id, asmt_ids)
      for comment in comments_info:
        self.assertEqual(comment["parent_id"], parent_obj_key.id)
        self.assertEqual(comment["parent_type"], "Assessment")
        expected_suffix = "asmt " + str(parent_obj_key.id)
        self.assertTrue(comment["description"].endswith(expected_suffix))

  SCOPING_OBJECT_FACTORIES = {
      factories.AccessGroupFactory,
      factories.DataAssetFactory,
      factories.FacilityFactory,
      factories.MarketFactory,
      factories.SystemFactory,
      factories.ProcessFactory,
      factories.ProductFactory,
      factories.ProjectFactory,
      factories.MetricFactory,
      factories.TechnologyEnvironmentFactory,
      factories.ProductGroupFactory,
      factories.OrgGroupFactory,
      factories.VendorFactory,
  }

  @ddt.data(
      factories.AccessGroupFactory,
      factories.ClauseFactory,
      factories.ControlFactory,
      factories.DataAssetFactory,
      factories.FacilityFactory,
      factories.MarketFactory,
      factories.ObjectiveFactory,
      factories.OrgGroupFactory,
      factories.SystemFactory,
      factories.ProcessFactory,
      factories.ProductFactory,
      factories.RequirementFactory,
      factories.VendorFactory,
      factories.IssueFactory,
      factories.PolicyFactory,
      factories.RegulationFactory,
      factories.StandardFactory,
      factories.ContractFactory,
      factories.RiskFactory,
      factories.ThreatFactory,
      factories.MetricFactory,
      factories.TechnologyEnvironmentFactory,
      factories.ProductGroupFactory,
  )
  @patch("ggrc.notifications.common.send_email")
  def test_models_comments(self, obj_factory, _):
    """Test setting notification entries for model comments.

    Check if the correct notification entries are created when a comment gets
    posted.
    """
    if obj_factory in self.SCOPING_OBJECT_FACTORIES:
      recipient_types = ["Admin", "Assignee", "Compliance Contacts",
                         "Product Managers", "Technical / Program Managers",
                         "Technical Leads", "System Owners", "Verifier",
                         "Legal Counsels"]
    else:
      recipient_types = ["Admin", "Primary Contacts", "Secondary Contacts"]
    person = all_models.Person.query.first()
    person_email = person.email

    with factories.single_commit():
      obj = obj_factory(
          recipients=",".join(recipient_types),
          send_by_default=False,
      )
      ac_roles = get_custom_roles_for(obj.type)
      for acr_id, acr_name in ac_roles.items():
        if acr_name in recipient_types:
          factories.AccessControlListFactory(
              ac_role_id=acr_id, object=obj, person=person
          )

    self.generator.generate_comment(
        obj, "", "some comment", send_notification="true")

    notifications, notif_data = common.get_daily_notifications()
    self.assertEqual(len(notifications), 1,
                     "Missing comment notification entry.")

    recip_notifs = notif_data.get(person_email, {})
    comment_notifs = recip_notifs.get("comment_created", {})
    self.assertEqual(len(comment_notifs), 1)

    # Check if correct revisions count is created
    revisions = Revision.query.filter(
        Revision.resource_type == 'Notification',
        Revision.resource_id.in_([n.id for n in notifications])
    )
    self.assertEqual(revisions.count(), 1)

    self.client.get("/_notifications/send_daily_digest")
    notifications = self._get_notifications(notif_type="comment_created").all()
    self.assertEqual(len(notifications), 0,
                     "Found a comment notification that was not sent.")

  def test_old_comments(self):
    """Test if notifications will be sent for mix of old and new comments"""
    cur_user = all_models.Person.query.filter_by(
        email="user@example.com"
    ).first()
    assigee_role_id = {
        v: k for k, v in get_custom_roles_for("Assessment").items()
    }["Assignees"]
    with factories.single_commit():
      assessment = factories.AssessmentFactory()
      factories.AccessControlListFactory(
          ac_role_id=assigee_role_id, person=cur_user, object=assessment
      )
    with freeze_time("2015-04-01 17:13:10"):
      self.generator.generate_comment(
          assessment, "", "some comment1", send_notification="true"
      )
    self.generator.generate_comment(
        assessment, "", "some comment2", send_notification="true"
    )
    response = self.client.get("/_notifications/show_pending")
    for comment in ["some comment1", "some comment2"]:
      self.assertIn(
          comment, response.data,
          "Information about comment '{}' absent in report".format(comment)
      )
