# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test deadlocks on parallel propagation requests."""

import threading

import flask

from ggrc import db
from ggrc.app import app
from ggrc.models import all_models
from ggrc.models.hooks.acl import propagation
from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestDeadlocks(TestCase):
  """Base test case for all propagation scenarios."""

  def setUp(self):
    super(TestDeadlocks, self).setUp()
    pm_role = all_models.AccessControlRole.query.filter_by(
        object_type="Program",
        name="Program Managers",
    ).one()
    with factories.single_commit():
      self.person = factories.PersonFactory()
      self.program = factories.ProgramFactory()
      self.audits = [factories.AuditFactory(program=self.program)
                     for _ in range(3)]
      self.rels = [
          factories.RelationshipFactory(source=self.program, destination=audit)
          for audit in self.audits
      ]

      self.parent_acl = factories.AccessControlListFactory(
          ac_role=pm_role,
          person=self.person,
          object=self.program,
      )
    db.session.execute(
        "DELETE FROM access_control_list WHERE parent_id IS NOT NULL",
    )
    db.session.commit()

  def test_deadlock(self):
    """No deadlocks occur if propagation for three Audits goes in parallel."""
    # Emulate connections from three parallel requests
    for relationship in self.rels:
      thread = threading.Thread(target=self._execute_propagation,
                                args=(relationship, ))
      thread.start()
      thread.join()

    db.session.rollback()

    self.assertEqual(
        all_models.AccessControlList.query.filter_by(
            parent_id=self.parent_acl.id,
        ).count(),
        3,
    )

  @staticmethod
  def _execute_propagation(relationship):
    """Execute propagation regarding relationship."""
    with app.app_context():
      flask.g.new_acl_ids = {}
      flask.g.new_relationship_ids = {relationship.id}
      flask.g.deleted_objects = {}

      propagation.propagate()
