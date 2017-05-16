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
    cls.audit = all_models.Audit.eager_query().filter(
        all_models.Audit.archived == 0).first()
    cls.archived_audit = all_models.Audit.eager_query().filter(
        all_models.Audit.archived == 1).first()

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
    """Test if users can edit an audit

       This is just a sanity check to make sure Editors can still edit all the
       fields except the archived column.
    """
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
