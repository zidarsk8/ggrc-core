# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for /query api endpoint."""

from os.path import abspath, dirname, join
from flask import json

from ggrc.app import app
from integration.ggrc import TestCase


THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, '../converters/test_csvs/')


class TestAdvancedQueryAPI(TestCase):
  """Basic tests for /query api."""

  @classmethod
  def setUpClass(cls):
    """Set up test cases for all tests."""
    TestCase.clear_data()
    # This imported file could be simplified a bit to speed up testing.
    cls.import_file("data_for_export_testing.csv")

  @classmethod
  def import_file(cls, filename):
    """Import a csv file.

    The file should contain all objects and mappings needed for writing proper
    query api tests.
    """
    client = app.test_client()
    client.get("/login")
    data = {"file": (open(join(CSV_DIR, filename)), filename)}
    headers = {"X-test-only": "false", "X-requested-by": "gGRC"}
    client.post("/_service/import_csv", data=data, headers=headers)

  def setUp(self):
    self.client.get("/login")

  def _post(self, data):
    headers = {'Content-Type': 'application/json', }
    return self.client.post("/query", data=json.dumps(data), headers=headers)

  def test_simple_export_query(self):
    """Test basic queries."""
    data = [{
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "="},
                "right": "Cat ipsum 1",
            },
        },
    }]
    response = json.loads(self._post(data).data)[0]
    programs = response.get("Program")
    self.assertIsNot(programs, None)
    self.assertEqual(programs["count"], 1)
    self.assertEqual(len(programs["values"]), 1)
    self.assertEqual(programs["values"][0]["title"], "Cat ipsum 1")

    data = [{
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "~"},
                "right": "1",
            },
        },
    }]
    response = json.loads(self._post(data).data)[0]
    programs = response.get("Program")
    self.assertIsNot(programs, None)
    self.assertEqual(programs["count"], 12)
    self.assertEqual(len(programs["values"]), 12)

  def test_basic_query(self):
    pass

  def test_basic_query_filter(self):
    pass

  def test_basic_query_pagination(self):
    pass

  def test_mapped_query(self):
    pass

  def test_mapped_query_filter(self):
    pass

  def test_mapped_query_pagination(self):
    pass

  def test_self_link(self):
    # It would be good if the api accepted get requests and we could add the
    # query into a get parameter, then each request would also get a self link
    # that could be tested to see that it truly returns what the original
    # request was.
    # In the end, instead of returning mapped object stubs like we do now, we'd
    # just return a self link for fetching those objects.
    pass
