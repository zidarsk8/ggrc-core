# coding: utf-8

# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for /query api endpoint."""


from ddt import data
from ddt import ddt
from ddt import unpack

from sqlalchemy import func

from ggrc import app
from ggrc import models
from ggrc.models import all_models
from ggrc import db

from integration.ggrc import TestCase
from integration.ggrc import generator
from integration.ggrc.query_helper import WithQueryApi
from integration.ggrc.models import factories
from integration.ggrc.models.factories import single_commit


# pylint: disable=super-on-old-class
@ddt
class TestAuditSnapshotQueries(TestCase, WithQueryApi):
  """Tests for /query api for Audit snapshots"""

  # objects mapped to assessments after set up:
  # Assessment 1 -- Market 1,
  # Assessment 2 -- Market 2, Control 1,
  # Assessment 3 -- Market 3, Control 1, Control 2
  # Assessment 4 -- Market 4, Control 1, Control 2, Control 3

  # Number of controls mapped to assessments
  ASSESSMENT_COUNTS = {
      "Assessment 1": 0,
      "Assessment 2": 1,
      "Assessment 3": 2,
      "Assessment 4": 3,
  }

  # Number of assessments mapped to controls
  CONTROL_COUNTS = {
      "Control 0": 0,  # unmapped control
      "Control 1": 3,
      "Control 2": 2,
      "Control 3": 1,
      "Control 4": 0,
      "Control 5": 0,
  }

  AUDIT_COUNTS = {
      "Control 0": 0,  # unmapped control
      "Control 1": 1,
      "Control 2": 1,
  }

  def setUp(self):
    """Log in before performing queries."""
    self.client.get("/login")
    self.client.post("/admin/full_reindex")

  @classmethod
  def setUpClass(cls):
    TestCase.clear_data()
    with app.app.app_context():
      cls._setup_objects()

  @staticmethod
  def _create_snapshotable_objects():
    """Create original objects that will be snapshotted."""
    text_cad = factories.CustomAttributeDefinitionFactory(
        title="text cad",
        definition_type="market",
    )
    date_cad = factories.CustomAttributeDefinitionFactory(
        title="date cad",
        definition_type="market",
        attribute_type="Date",
    )

    for i in range(5):
      factories.ControlFactory(title="Control {}".format(i + 1))
      factories.OrgGroupFactory()
      market = factories.MarketFactory(title="Market {}".format(i + 1))
      factories.CustomAttributeValueFactory(
          custom_attribute=date_cad,
          attributable=market,
          attribute_value="2016-11-0{}".format(i + 3),
      )
      factories.CustomAttributeValueFactory(
          custom_attribute=text_cad,
          attributable=market,
          attribute_value="2016-11-0{}".format(i + 1),
      )

  @classmethod
  def _setup_objects(cls):
    """Create and reindex objects needed for tests"""
    cls._create_snapshotable_objects()

    revisions = models.Revision.query.filter(
        models.Revision.resource_type.in_(["OrgGroup", "Market", "Control"]),
        models.Revision.id.in_(
            db.session.query(func.max(models.Revision.id)).group_by(
                models.Revision.resource_type,
                models.Revision.resource_id,
            )
        ),
    )

    audit = factories.AuditFactory()

    snapshots = [
        factories.SnapshotFactory(
            child_id=revision.resource_id,
            child_type=revision.resource_type,
            revision=revision,
            parent=audit,
        )
        for revision in revisions
    ]

    snapshot_map = {snapshot.revision.content["title"]: snapshot
                    for snapshot in snapshots}

    for snapshot in snapshots:
      factories.RelationshipFactory(
          source=audit,
          destination=snapshot,
      )

    # create Assessments and issues and map some snapshots to them
    # Markets and Controls represent snapshots of those objects.

    assessment_issues = (
        factories.AssessmentFactory,
        factories.IssueFactory,
    )
    for i in range(4):
      for factory in assessment_issues:
        # pylint: disable=protected-access
        obj = factory(
            title="{} {}".format(factory._meta.model.__name__, i + 1),
            audit=audit if factory != factories.IssueFactory else None,
        )
        factories.RelationshipFactory(
            source=audit if i % 2 == 0 else obj,
            destination=audit if i % 2 == 1 else obj,
        )

        market = snapshot_map["Market {}".format(i + 1)]
        factories.RelationshipFactory(
            source=market if i % 2 == 0 else obj,
            destination=market if i % 2 == 1 else obj,
        )
        for j in range(i):
          control = snapshot_map["Control {}".format(j + 1)]
          factories.RelationshipFactory(
              source=control if i % 2 == 0 else obj,
              destination=control if i % 2 == 1 else obj,
          )

    # Create an unmapped control for base tests
    factories.ControlFactory(title="Control 0")

  def test_basic_snapshot_query(self):
    """Test fetching all snapshots for a given Audit."""
    result = self._post([
        {
            "object_name": "Snapshot",
            "filters": {
                "expression": self._get_model_expression(),
                "keys": [],
                "order_by": {"keys": [], "order": "", "compare": None}
            }
        }
    ])
    self.assertEqual(len(result.json[0]["Snapshot"]["values"]), 5)

    result = self._post([
        {
            "object_name": "Snapshot",
            "filters": {
                "expression": self._get_model_expression("OrgGroup"),
                "keys": [],
                "order_by": {"keys": [], "order": "", "compare": None}
            }
        }
    ])
    self.assertEqual(len(result.json[0]["Snapshot"]["values"]), 5)

  def test_snapshot_attribute_filter(self):
    """Test filtering snapshots on object attributes."""
    market_title = models.Market.query.first().title
    result = self._post([
        {
            "object_name": "Snapshot",
            "filters": {
                "expression": {
                    "left": self._get_model_expression(),
                    "op": {"name": "AND"},
                    "right": {
                        "left": "title",
                        "op": {"name": "="},
                        "right": market_title,
                    },
                },
                "keys": [],
                "order_by": {"keys": [], "order": "", "compare": None}
            }
        }
    ])
    self.assertEqual(len(result.json[0]["Snapshot"]["values"]), 1)
    content = result.json[0]["Snapshot"]["values"][0]["revision"]["content"]
    self.assertEqual(
        content["title"],
        market_title,
    )

    result = self._post([
        {
            "object_name": "Snapshot",
            "filters": {
                "expression": {
                    "left": self._get_model_expression("OrgGroup"),
                    "op": {"name": "AND"},
                    "right": {
                        "left": "title",
                        "op": {"name": "!="},
                        "right": models.OrgGroup.query.first().title,
                    },
                },
                "keys": [],
                "order_by": {"keys": [], "order": "", "compare": None}
            }
        }
    ])
    self.assertEqual(len(result.json[0]["Snapshot"]["values"]), 4)

  def test_snapshot_date_ca_filter(self):
    """Test filtering snapshots by date custom attributes."""
    result = self._post([
        {
            "object_name": "Snapshot",
            "filters": {
                "expression": {
                    "left": self._get_model_expression(),
                    "op": {"name": "AND"},
                    "right": {
                        "left": {
                            "left": "text cad",
                            "op": {"name": "="},
                            "right": "2016-11-01",  # one match
                        },
                        "op": {"name": "OR"},
                        "right": {
                            "left": "date cad",
                            "op": {"name": ">"},
                            "right": "11/05/2016",  # 2 matches
                        },
                    },
                },
                "keys": [],
                "order_by": {"keys": [], "order": "", "compare": None}
            }
        }
    ])
    self.assertEqual(len(result.json[0]["Snapshot"]["values"]), 3)

  @data(*CONTROL_COUNTS.items())
  def test_assesessment_relationships(self, test_data):
    """Test relationships between Assessments and original objects."""
    title, expected = test_data
    control = models.Control.query.filter_by(title=title).first()

    result = self._post([
        {
            "object_name": "Assessment",
            "filters": {
                "expression": {
                    "object_name": "Control",
                    "op": {"name": "relevant"},
                    "ids": [control.id]
                },
                "keys": [],
                "order_by": {"keys": [], "order": "", "compare": None}
            }
        }
    ])
    count = len(result.json[0]["Assessment"]["values"])
    self.assertEqual(count, expected,
                     "Invalid related Assessment count for '{}'."
                     "Expected {}, got {}".format(title, expected, count))

  @data(*ASSESSMENT_COUNTS.items())
  def test_original_objects(self, test_data):
    """Test relationships between original objects and Assessments."""
    title, expected = test_data
    assessment = models.Assessment.query.filter_by(title=title).first()

    result = self._post([
        {
            "object_name": "Control",
            "filters": {
                "expression": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": [assessment.id]
                },
                "keys": [],
                "order_by": {"keys": [], "order": "", "compare": None}
            }
        }
    ])
    count = len(result.json[0]["Control"]["values"])
    self.assertEqual(count, expected,
                     "Invalid related Control count for '{}'."
                     "Expected {}, got {}".format(title, expected, count))

  def test_audit_empty_queries(self):
    """Test Audit relationship for irrelevant objects."""
    result = self._post([
        {
            "object_name": "Audit",
            "filters": {
                "expression": {
                    "object_name": "Control",
                    "op": {"name": "relevant"},
                    "ids": [-1]
                },
                "keys": [],
                "order_by": {"keys": [], "order": "", "compare": None}
            }
        }
    ])
    count = len(result.json[0]["Audit"]["values"])
    expected = 0
    self.assertEqual(count, expected,
                     "Invalid related Audit count for Audit."
                     "Expected {}, got {}".format(expected, count))

  def test_audit_parent_relationships(self):
    """Test snapshotted object relationship to Audits."""
    audit = models.Audit.query.first()
    result = self._post([
        {
            "object_name": "Control",
            "filters": {
                "expression": {
                    "object_name": "Audit",
                    "op": {"name": "relevant"},
                    "ids": [audit.id]
                },
                "keys": [],
                "order_by": {"keys": [], "order": "", "compare": None}
            }
        }
    ])
    count = len(result.json[0]["Control"]["values"])
    expected = 5  # Audit should contain 5 control snapshots
    self.assertEqual(count, expected,
                     "Invalid related Control count for Audit."
                     "Expected {}, got {}".format(expected, count))

  @data(*AUDIT_COUNTS.items())
  def test_audit_child_relationships(self, test_data):
    """Test audit relationships for snapshotted objects."""
    title, expected = test_data
    control = models.Control.query.filter_by(title=title).first()

    result = self._post([
        {
            "object_name": "Audit",
            "filters": {
                "expression": {
                    "object_name": "Control",
                    "op": {"name": "relevant"},
                    "ids": [control.id]
                },
                "keys": [],
                "order_by": {"keys": [], "order": "", "compare": None}
            }
        }
    ])
    count = len(result.json[0]["Audit"]["values"])
    self.assertEqual(count, expected,
                     "Invalid related Audit count for '{}'."
                     "Expected {}, got {}".format(title, expected, count))

  @staticmethod
  def _get_model_expression(model_name="Market"):
    return {
        "left": {
            "left": "child_type",
            "op": {"name": "="},
            "right": model_name,
        },
        "op": {"name": "AND"},
        "right": {
            "object_name": "Audit",
            "op": {"name": "relevant"},
            "ids": [models.Audit.query.first().id]
        }
    }


@ddt
class TestIssueRelevantFilter(TestCase, WithQueryApi):
  """Test suite to check both Snapshots and Snapshottables in relevant."""
  # pylint: disable=invalid-name

  def setUp(self):
    super(TestIssueRelevantFilter, self).setUp()
    self.client.get("/login")

    self.snapshottable = factories.ObjectiveFactory()
    revision = all_models.Revision.query.filter_by(
        resource_id=self.snapshottable.id,
        resource_type=self.snapshottable.type,
    ).first()

    with factories.single_commit():
      self.control = factories.ControlFactory()
      self.audit = factories.AuditFactory()
      self.issue = factories.IssueFactory()
      self.snapshot = factories.SnapshotFactory(
          parent=self.audit,
          child_id=self.snapshottable.id,
          child_type=self.snapshottable.type,
          revision_id=revision.id,
      )

      factories.RelationshipFactory(source=self.issue,
                                    destination=self.control)
      factories.RelationshipFactory(source=self.issue, destination=self.audit)
      factories.RelationshipFactory(source=self.issue,
                                    destination=self.snapshot)

    self.objects = {
        "Issue": self.issue,
        "Control": self.control,
        "Snapshot": self.snapshot,
        "Snapshottable": self.snapshottable,
    }

  @staticmethod
  def _make_relevant_filter(target_type, relevant_obj):
    return {"object_name": target_type,
            "type": "ids",
            "filters": {"expression": {
                "op": {"name": "relevant"},
                "object_name": relevant_obj.type,
                "ids": [relevant_obj.id],
            }}}

  @data(("Issue", "Control"),
        ("Control", "Issue"),
        ("Issue", "Snapshot"),
        ("Snapshot", "Issue"),
        ("Issue", "Snapshottable"),
        ("Snapshottable", "Issue"))
  @unpack
  def test_relevant_issue_snapshottable(self, target, relevant_to):
    """Relevant filter returns Snapshots and Snapshottables for Issue."""
    target_obj = self.objects[target]
    relevant_obj = self.objects[relevant_to]
    target_id = target_obj.id

    result = self._get_first_result_set(
        self._make_relevant_filter(target_obj.type, relevant_obj),
        target_obj.type, "ids",
    )

    self.assertEqual(result, [target_id])


@ddt
class TestSnapshotIndexing(TestCase, WithQueryApi):
  """Test suite to check indexing of special fields in Snapshots."""

  def setUp(self):
    self.clear_data()
    super(TestSnapshotIndexing, self).setUp()
    self.generator = generator.ObjectGenerator()
    self.client.get("/login")

  def _create_audit(self, program, title):
    """Make a POST to create an Audit.

    AuditFactory doesn't trigger Snapshotter
    """
    self.generator.generate_object(models.Audit, {
        "title": title,
        "program": {"id": program.id},
        "status": "Planned",
        "snapshots": {
            "operation": "create",
        }
    })

  def test_process_network_zone(self):
    """Process Snapshots are filtered and sorted by "network zone"."""
    program = factories.ProgramFactory()
    nz_core = db.session.query(models.Option).filter_by(title="Core").one()
    nz_prod = db.session.query(models.Option).filter_by(title="Prod").one()
    process_nz_core = factories.ProcessFactory(network_zone=nz_core)
    process_nz_prod = factories.ProcessFactory(network_zone=nz_prod)
    factories.RelationshipFactory(source=program, destination=process_nz_core)
    factories.RelationshipFactory(source=program, destination=process_nz_prod)
    process_nz_core_id = process_nz_core.id
    process_nz_prod_id = process_nz_prod.id

    self._create_audit(program=program, title="test_process_network_zone")

    process_nz_core_result = self._get_first_result_set(
        self._make_snapshot_query_dict("Process",
                                       expression=["Network Zone", "=",
                                                   "Core"]),
        "Snapshot",
    )
    self.assertEqual(process_nz_core_result["count"], 1)
    self.assertTrue(all(snap["revision"]["content"]["network_zone"]
                        ["title"] == "Core"
                        for snap in process_nz_core_result["values"]))
    process_nz_prod_result = self._get_first_result_set(
        self._make_snapshot_query_dict("Process",
                                       expression=["Network Zone", "=",
                                                   "prod"]),
        "Snapshot",
    )
    self.assertEqual(process_nz_prod_result["count"], 1)
    self.assertTrue(all(snap["revision"]["content"]["network_zone"]
                        ["title"] == "Prod"
                        for snap in process_nz_prod_result["values"]))

    order_by_nz_result = self._get_first_result_set(
        self._make_snapshot_query_dict("Process",
                                       order_by=[{"name": "Network Zone"}]),
        "Snapshot",
    )
    self.assertEqual(order_by_nz_result["count"], 2)
    self.assertListEqual([snap["child_id"]
                          for snap in order_by_nz_result["values"]],
                         [process_nz_core_id, process_nz_prod_id])

  def _add_owner(self, ownable, person_id):
    """Create ACL for provided object and person."""
    factories.AccessControlPersonFactory(
        ac_list=ownable.acr_name_acl_map["Admin"],
        person_id=person_id,
    )

  def assert_rows_number_in_search(self, field, value, expected_num):
    """Assert expected_num of rows found by that value search"""
    control_user1_result = self._get_first_result_set(
        self._make_snapshot_query_dict(
            "Control", expression=[field, "=", value]
        ),
        "Snapshot",
    )
    self.assertEqual(control_user1_result["count"], expected_num)

  def _test_contact_field(self, contact_name_field, search_field):
    """Util function for test for filtering by contact fields"""
    person_name = "name"
    person_email = "email@addr.com"
    program = factories.ProgramFactory()
    program_id = program.id
    control_kwargs = {
        contact_name_field: factories.PersonFactory(name=person_name,
                                                    email=person_email),
    }
    control = factories.ControlFactory(**control_kwargs)
    factories.RelationshipFactory(source=program, destination=control)
    program = models.Program.query.filter_by(id=program_id).one()
    self._create_audit(program=program, title="some title")
    self.assert_rows_number_in_search(search_field, person_name, 1)
    self.assert_rows_number_in_search(search_field, person_email, 1)
    self.assert_rows_number_in_search(search_field,
                                      "negative_" + person_name,
                                      0)
    self.assert_rows_number_in_search(search_field,
                                      "negative_" + person_email,
                                      0)

  def test_control_owners(self):
    """Control Snapshots are filtered and sorted by Owners."""
    with single_commit():
      program = factories.ProgramFactory()
      controls = [factories.ControlFactory(),
                  factories.ControlFactory()]
      people = [
          factories.PersonFactory(name="Ann", email="email1@example.com"),
          factories.PersonFactory(name="Bob", email="email2@example.com"),
          factories.PersonFactory(name="Carl", email="email3@example.com")
      ]
      program_id = program.id
      control_ids = [c.id for c in controls]
      people_ids = [p.id for p in people]

      factories.RelationshipFactory(source=program, destination=controls[0])
      factories.RelationshipFactory(source=program, destination=controls[1])

      self._add_owner(controls[0], people_ids[0])
      self._add_owner(controls[0], people_ids[2])
      self._add_owner(controls[1], people_ids[0])
      self._add_owner(controls[1], people_ids[1])

    program = models.Program.query.filter_by(id=program_id).one()

    control_revisions = models.Revision.query.filter_by(
        resource_type="Control"
    ).all()
    for c_rev in control_revisions:
      c_rev.content = models.Control.query.get(c_rev.resource_id).log_json()
      db.session.add(c_rev)
    db.session.commit()
    self._create_audit(program=program, title="some title")

    control_user1_result = self._get_first_result_set(
        self._make_snapshot_query_dict("Control",
                                       expression=["Admin", "=", "Ann"]),
        "Snapshot",
    )
    self.assertEqual(control_user1_result["count"], 2)

    def owner_ids(snapshot):
      """Shortcut to get owners list of a snapshotted object."""
      owners = []
      admin_role_id = models.AccessControlRole.query.filter_by(
          name="Admin",
          object_type=snapshot["revision"]["resource_type"]
      ).first().id
      for acl in snapshot["revision"]["content"]["access_control_list"]:
        if acl["ac_role_id"] == admin_role_id:
          owners.append(acl["person_id"])
      return owners

    self.assertTrue(all(people_ids[0] in {o for o in owner_ids(snap)}
                        for snap in control_user1_result["values"]))

    control_user2_result = self._get_first_result_set(
        self._make_snapshot_query_dict("Control",
                                       expression=["admin", "=", "Bob"]),
        "Snapshot",
    )
    self.assertEqual(control_user2_result["count"], 1)
    self.assertTrue(all(people_ids[1] in {o for o in owner_ids(snap)}
                        for snap in control_user2_result["values"]))

    order_by_owners_result = self._get_first_result_set(
        self._make_snapshot_query_dict("Control",
                                       order_by=[{"name": "admin"}]),
        "Snapshot"
    )
    self.assertEqual(order_by_owners_result["count"], 2)
    self.assertListEqual([snap["child_id"]
                          for snap in order_by_owners_result["values"]],
                         [control_ids[1], control_ids[0]])

  @data(
      ("updated_at", ("updated_at", "Last Updated Date", "last updated date")),
      ("created_at", ("updated_at", "Created Date", "Created Date")),
  )
  @unpack
  def test_filter_by_dt_field(self, field, aliases):
    """Control Snapshots are filtered by datetime fields"""
    program = factories.ProgramFactory()
    control = factories.ControlFactory()
    datetime_value = getattr(control, field)
    factories.RelationshipFactory(source=program, destination=control)
    self._create_audit(program=program, title="some title")
    for date_string in self.generate_date_strings(datetime_value):
      for alias in aliases:
        query_dict = self._make_snapshot_query_dict(
            "Control",
            expression=[alias, "=", date_string]
        )
        filtered_controls = self._get_first_result_set(query_dict, "Snapshot")
        self.assertEqual(
            filtered_controls["count"],
            1,
            "empty results for alias {} and value {}".format(
                alias, date_string
            )
        )

  def test_person_ca(self):
    """Control Snapshots are filtered and sorted by Person CA."""
    with factories.single_commit():
      program = factories.ProgramFactory()
      person1 = factories.PersonFactory(name="Ann", email="email1@example.com")
      person2 = factories.PersonFactory(name="Bob", email="email2@example.com")

    with factories.single_commit():
      control1 = factories.ControlFactory()
      control2 = factories.ControlFactory()
      cad = factories.CustomAttributeDefinitionFactory(
          definition_type="control",
          definition_id=None,
          attribute_type="Map:Person",
          title="Global Person CA",
      )
      factories.CustomAttributeValueFactory(
          attributable=control1,
          custom_attribute=cad,
          attribute_value=person2.type,
          attribute_object_id=person2.id,
      )
      factories.CustomAttributeValueFactory(
          attributable=control2,
          custom_attribute=cad,
          attribute_value=person1.type,
          attribute_object_id=person1.id,
      )
      control1_id = control1.id
      control2_id = control2.id

      factories.RelationshipFactory(source=program, destination=control1)
      factories.RelationshipFactory(source=program, destination=control2)

    self._create_audit(program=program, title="test_person_ca")

    controls_user1 = self._get_first_result_set(
        self._make_snapshot_query_dict(
            "Control",
            expression=["Global Person CA", "=", "Ann"]
        ),
        "Snapshot", "values",
    )
    self.assertItemsEqual([c["child_id"] for c in controls_user1],
                          [control2_id])

    controls_user2 = self._get_first_result_set(
        self._make_snapshot_query_dict(
            "Control",
            expression=["Global Person CA", "=", "email2@example.com"]
        ),
        "Snapshot", "values",
    )
    self.assertSetEqual({c["child_id"] for c in controls_user2},
                        {control1_id})

    order_by_person_ca_result = self._get_first_result_set(
        self._make_snapshot_query_dict(
            "Control",
            order_by=[{"name": "Global Person CA"}]
        ),
        "Snapshot"
    )
    self.assertEqual(order_by_person_ca_result["count"], 2)
    self.assertListEqual([snap["child_id"]
                          for snap in order_by_person_ca_result["values"]],
                         [control2_id, control1_id])

  @data(
      "Test Role Name",
      "TEST ROLE NAME",
      "test role name",
  )
  def test_acl_filter(self, test_role_name):
    """Control Snapshots are filtered and sorted by ACL Role."""
    factories.AccessControlRoleFactory(
        name=test_role_name,
        object_type="Control"
    )
    with factories.single_commit():
      program = factories.ProgramFactory()
      person1 = factories.PersonFactory(name="Ann", email="email1@example.com")
      control1 = factories.ControlFactory()
      control2 = factories.ControlFactory()
      program_id = program.id
      control1_id = control1.id
      control2_id = control2.id
      factories.RelationshipFactory(source=program, destination=control1)
      factories.RelationshipFactory(source=program, destination=control2)
      factories.AccessControlPersonFactory(
          ac_list=control1.acr_name_acl_map[test_role_name],
          person=person1,
      )
    revision = all_models.Revision.query.filter(
        all_models.Revision.resource_type == "Control",
        all_models.Revision.resource_id == control1_id
    ).order_by(all_models.Revision.updated_at.desc()).first()
    revision.content = control1.log_json()
    db.session.add(revision)
    db.session.commit()
    program = models.Program.query.filter_by(id=program_id).one()
    self._create_audit(program=program, title="some title")
    control_user1_result = self._get_first_result_set(
        self._make_snapshot_query_dict(
            "Control",
            expression=['{}'.format(test_role_name), "=", "Ann"]
        ),
        "Snapshot",
    )
    self.assertEqual(control_user1_result["count"], 1)
    snaps_dict = dict(
        all_models.Snapshot.query.filter(
            all_models.Snapshot.child_type == "Control"
        ).values("child_id", "id")
    )
    self.assertIn(snaps_dict[control1_id],
                  [i["id"] for i in control_user1_result["values"]])
    self.assertNotIn(snaps_dict[control2_id],
                     [i["id"] for i in control_user1_result["values"]])

  def test_categories_filter(self):
    """Control Snapshots are filtered by categories."""
    with factories.single_commit():
      program = factories.ProgramFactory()
      program_id = program.id

      category = factories.ControlCategoryFactory()
      category_id = category.id
      control = factories.ControlFactory()
      control.categories.append(category)
      control_id = control.id
      factories.RelationshipFactory(source=program, destination=control)
      revision = all_models.Revision.query.filter(
          all_models.Revision.resource_type == "Control",
          all_models.Revision.resource_id == control_id
      ).order_by(all_models.Revision.updated_at.desc()).first()
      revision.content = control.log_json()

    program = models.Program.query.filter_by(id=program_id).one()
    self._create_audit(program=program, title="some title")
    category = models.ControlCategory.query.get(category_id)
    control_result = self._get_first_result_set(
        self._make_snapshot_query_dict(
            "Control",
            expression=["categories", "=", "{}".format(category.name)]
        ),
        "Snapshot",
    )
    self.assertEqual(control_result["count"], 1)
    snapshot_categories = \
        control_result["values"][0]["revision"]["content"]["categories"]
    self.assertEqual(category.name, snapshot_categories[0]["display_name"])
