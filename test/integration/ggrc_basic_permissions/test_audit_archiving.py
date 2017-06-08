# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test Archived Audit"""

from os.path import abspath
from os.path import dirname
from os.path import join
from ddt import data, ddt, unpack
from ggrc.app import app  # NOQA pylint: disable=unused-import
from ggrc.app import db
from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc.api_helper import Api
from integration.ggrc.models import factories


CONTEXT_OBJECTS = ('issue', 'assessment', 'template')
ARCHIVED_CONTEXT_OBJECTS = (
    'archived_issue',
    'archived_assessment',
    'archived_template')

class TestAuditArchivingBase(TestCase):
  """Base class for testing archived audits"""
  CSV_DIR = join(abspath(dirname(__file__)), "test_csvs")

  @classmethod
  def setUpClass(cls):
    """Prepare data needed to run the tests"""
    TestCase.clear_data()
    cls.response = cls._import_file("audit_rbac.csv")
    cls.people = {
        person.name: person for person in all_models.Person.eager_query().all()
    }
    created_objects = (
        (all_models.Audit, all_models.Audit.archived == 0, 'audit'),
        (all_models.Audit, all_models.Audit.archived == 1, 'archived_audit'),
        (all_models.Issue, all_models.Issue.slug == 'PMRBACISSUE-1', 'issue'),
        (all_models.Issue, all_models.Issue.slug == 'PMRBACISSUE-2',
         'archived_issue'),
        (all_models.Assessment,
         all_models.Assessment.slug == 'PMRBACASSESSMENT-1', 'assessment'),
        (all_models.Assessment,
         all_models.Assessment.slug == 'PMRBACASSESSMENT-2',
         'archived_assessment')
    )
    for obj, cond, name in created_objects:
      setattr(cls, name, obj.eager_query().filter(cond).first())

    revision = all_models.Revision.query.filter(
        all_models.Revision.resource_type == 'Objective').first()
    cls.rev_id = revision.id

    # Create snapshot objects:
    for audit, name in ((cls.audit, 'snapshot'),
                        (cls.archived_audit, 'archived_snapshot')):
      setattr(cls, name, factories.SnapshotFactory(
          child_id=revision.resource_id,
          child_type=revision.resource_type,
          revision=revision,
          parent=audit,
          context=audit.context,
      ))

    # Create asessment template objects:
    for audit, name in ((cls.audit, 'template'),
                        (cls.archived_audit, 'archived_template')):
      template = factories.AssessmentTemplateFactory(
          context=audit.context,
      )
      factories.RelationshipFactory(
          source=audit,
          destination=template,
          context=audit.context
      )
      setattr(cls, name, template)
    # Refresh objects in the session
    for obj in db.session:
      db.session.refresh(obj)

  def setUp(self):
    """Imports test_csvs/audit_rbac.csv needed by the tests"""
    self._check_csv_response(self.response, {})
    self.api = Api()
    self.client.get("/login")
    db.engine.execute("""
      UPDATE audits
         SET archived = 0,
             description = ""
      WHERE title = '2016: Program Manager Audit RBAC Test - Audit 1'
    """)
    db.engine.execute("""
      UPDATE audits
         SET archived = 1,
             description = ""
       WHERE title = '2016: Program Manager Audit RBAC Test - Audit 2'
    """)
    db.engine.execute("""
      UPDATE issues
         SET title = slug
    """)
    db.engine.execute("""
      UPDATE assessments
         SET title = slug
    """)
    db.engine.execute("""
      UPDATE assessment_templates
         SET title = slug
    """)
    db.engine.execute("""
      UPDATE snapshots
         SET revision_id = {}
    """.format(self.rev_id))


@ddt
class TestAuditArchiving(TestAuditArchivingBase):
  """Tests Archived Audits

  Tests the following cases:

  1. Audit can only be archived by Global Admin or Program Manager
  2. Audit can only be unarchived by Global Admin or Program Manager
  """

  @data(
      ('Admin', 200),
      ('Editor', 403),
      ('Reader', 403),
      ('Creator', 403),
      ('Creator PM', 200),
      ('Creator PE', 403),
      ('Creator PR', 403)
  )
  @unpack
  def test_setting_archived_state(self, person, status):
    """Test if users can archive an audit"""
    self.api.set_user(self.people[person])
    audit_json = {
        "archived": True
    }
    response = self.api.put(self.audit, audit_json)
    assert response.status_code == status, \
        "{} put returned {} instead of {}".format(
            person, response.status, status)
    if status != 200:
      # if editing is allowed check if edit was correctly saved
      return

    assert response.json["audit"].get("archived", None) is True, \
        "Audit has not been archived correctly {}".format(
        response.json["audit"])

  @data(
      ('Admin', 200),
      ('Editor', 403),
      ('Reader', 403),
      ('Creator', 403),
      ('Creator PM', 200),
      ('Creator PE', 403),
      ('Creator PR', 403)
  )
  @unpack
  def test_unsetting_archived_state(self, person, status):
    """Test if users can unarchive an audit"""

    self.api.set_user(self.people[person])
    audit_json = {
        "archived": False
    }
    response = self.api.put(self.archived_audit, audit_json)
    assert response.status_code == status, \
        "{} put returned {} instead of {}".format(
            person, response.status, status)
    if status != 200:
      # if editing is allowed check if edit was correctly saved
      return

    assert response.json["audit"].get("archived", None) is False, \
        "Audit has not been unarchived correctly {}".format(
        response.json["audit"])


@ddt
class TestArchivedAudit(TestAuditArchivingBase):
  """Tests Archived Audits

  Tests the following cases:

  1. Once archived the audit cannot be edited by anyone
  2. Once archived the objects with the audit context cannot be edited
     by anyone
  3. Once archived no new objects can be created in the audit context
  4. Once archived no mappings can be created in the audit context
  """

  @data(
      ('Admin', 200, 'audit'),
      ('Editor', 200, 'audit'),
      ('Reader', 403, 'audit'),
      ('Creator', 403, 'audit'),
      ('Creator PM', 200, 'audit'),
      ('Creator PE', 200, 'audit'),
      ('Creator PR', 403, 'audit'),
      ('Admin', 403, 'archived_audit'),
      ('Editor', 403, 'archived_audit'),
      ('Reader', 403, 'archived_audit'),
      ('Creator', 403, 'archived_audit'),
      ('Creator PM', 403, 'archived_audit'),
      ('Creator PE', 403, 'archived_audit'),
      ('Creator PR', 403, 'archived_audit')
  )
  @unpack
  def test_audit_editing(self, person, status, audit_type):
    """Test if users can edit an audit"""
    audit = getattr(self, audit_type)

    self.api.set_user(self.people[person])
    audit_json = {
        "description": "New"
    }
    response = self.api.put(audit, audit_json)
    assert response.status_code == status, \
        "{} put returned {} instead of {} for {}".format(
            person, response.status, status, audit_type)
    if status != 200:
      # if editing is allowed check if edit was correctly saved
      return

    assert response.json["audit"].get("description", None) == "New", \
        "Audit has not been updated correctly {}".format(
        response.json["audit"])

  @data(
      ('Admin', 200, CONTEXT_OBJECTS),
      ('Editor', 200, CONTEXT_OBJECTS),
      ('Reader', 403, CONTEXT_OBJECTS),
      ('Creator', 403, CONTEXT_OBJECTS),
      ('Creator PM', 200, CONTEXT_OBJECTS),
      ('Creator PE', 200, CONTEXT_OBJECTS),
      ('Creator PR', 403, CONTEXT_OBJECTS),
      ('Admin', 403, ARCHIVED_CONTEXT_OBJECTS),
      ('Editor', 403, ARCHIVED_CONTEXT_OBJECTS),
      ('Reader', 403, ARCHIVED_CONTEXT_OBJECTS),
      ('Creator', 403, ARCHIVED_CONTEXT_OBJECTS),
      ('Creator PM', 403, ARCHIVED_CONTEXT_OBJECTS),
      ('Creator PE', 403, ARCHIVED_CONTEXT_OBJECTS),
      ('Creator PR', 403, ARCHIVED_CONTEXT_OBJECTS)
  )
  @unpack
  def test_audit_context_editing(self, person, status, objects):
    """Test if users can edit objects in the audit context"""
    self.api.set_user(self.people[person])
    for obj in objects:
      obj_instance = getattr(self, obj)
      json = {
          "title": "New"
      }
      response = self.api.put(obj_instance, json)
      assert response.status_code == status, \
          "{} put returned {} instead of {} for {}".format(
              person, response.status, status, obj)
      if status != 200:
        # if editing is allowed check if edit was correctly saved
        continue
      table_singular = obj_instance._inflector.table_singular
      assert response.json[table_singular].get("title", None) == "New", \
          "{} has not been updated correctly {}".format(
          obj,
          response.json[obj])

  @data(
      ('Admin', 200, 'snapshot'),
      ('Editor', 200, 'snapshot'),
      ('Reader', 403, 'snapshot'),
      ('Creator', 403, 'snapshot'),
      ('Creator PM', 200, 'snapshot'),
      ('Creator PE', 200, 'snapshot'),
      ('Creator PR', 403, 'snapshot'),
      ('Admin', 403, 'archived_snapshot'),
      ('Editor', 403, 'archived_snapshot'),
      ('Reader', 403, 'archived_snapshot'),
      ('Creator', 403, 'archived_snapshot'),
      ('Creator PM', 403, 'archived_snapshot'),
      ('Creator PE', 403, 'archived_snapshot'),
      ('Creator PR', 403, 'archived_snapshot')
  )
  @unpack
  def test_audit_snapshot_editing(self, person, status, obj):
    """Test if users can edit objects in the audit context"""
    self.api.set_user(self.people[person])
    obj_instance = getattr(self, obj)
    json = {
        "update_revision": "latest"
    }

    response = self.api.put(obj_instance, json)
    assert response.status_code == status, \
        "{} put returned {} instead of {} for {}".format(
            person, response.status, status, obj)
    if status != 200:
      # if editing is allowed check if edit was correctly saved
      return
    assert response.json[obj].get("revision_id", None) > self.rev_id, \
        "{} has not been updated to the latest revision {}".format(
        obj,
        response.json[obj])
