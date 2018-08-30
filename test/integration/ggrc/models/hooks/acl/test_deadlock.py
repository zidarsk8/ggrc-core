# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test deadlocks on parallel propagation requests."""

import mock

import flask

from ggrc import db
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

  def test_deadlock(self):
    """No deadlocks occur if propagation for three Audits goes in parallel."""

    new_conn = db.engine.begin

    # Emulate connections from three parallel requests
    with new_conn() as conn0, new_conn() as conn1, new_conn() as conn2:
      for rel, conn in zip(self.rels, [conn0, conn1, conn2]):
        with mock.patch("ggrc.access_control.utils.db.session.execute",
                        conn.execute):
          flask.g.new_acl_ids = {}
          flask.g.new_relationship_ids = {rel.id}
          flask.g.deleted_objects = {}

          propagation.propagate()

    self.assertEqual(
        all_models.AccessControlList.query.filter_by(
            parent_id=self.parent_acl.id,
        ).count(),
        3,
    )
