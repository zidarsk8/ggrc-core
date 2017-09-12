# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

# pylint: disable=maybe-no-member

"""Test System import."""

import tempfile
import csv

from ggrc.models import all_models

from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestSystemImport(TestCase):
  """System import tests."""

  def test_import_duble_rows(self):
    """Update Admin ACL over import for same object in 2 different rows."""
    role = all_models.AccessControlRole.query.filter(
        all_models.AccessControlRole.name == "Admin",
        all_models.AccessControlRole.object_type == "System",
    ).one()
    with factories.single_commit():
      system = factories.SystemFactory(title="Test Title", slug="Test")
      admin_person = factories.PersonFactory()
      factories.AccessControlListFactory(ac_role=role,
                                         object=system,
                                         person=admin_person)
      update_person = factories.PersonFactory()
    with tempfile.NamedTemporaryFile(dir=self.CSV_DIR, suffix=".csv") as tmp:
      writer = csv.writer(tmp)
      writer.writerow(["Object type"])
      writer.writerow(["System", "Code*", "Title*", "Admin*"])
      data = ["", system.slug, system.title, update_person.email]
      writer.writerow(data)
      writer.writerow(data)
      tmp.seek(0)
      resp = self.import_file(tmp.name, dry_run=True)
    expected_data = [{
        u'ignored': 1,
        u'updated': 1,
        u'block_errors': [],
        u'name': u'System',
        u'created': 0,
        u'deleted': 0,
        u'deprecated': 0,
        u'row_warnings': [],
        u'rows': 2,
        u'block_warnings': [],
        u'row_errors': [
            u"Lines 3, 4 have same Code 'Test'. Line 4 will be ignored.",
            u"Lines 3, 4 have same Title 'Test Title'. Line 4 will be ignored."
        ]
    }]
    self.assertEqual(expected_data, resp)
