# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for /query api endpoint."""

from os.path import abspath, dirname, join
from flask import json
from nose.plugins.skip import SkipTest

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
    """Make a POST to /query endpoint."""
    if not isinstance(data, list):
      data = [data]
    headers = {'Content-Type': 'application/json', }
    return self.client.post("/query", data=json.dumps(data), headers=headers)

  def test_simple_export_query(self):
    """Test basic queries."""
    data = {
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "="},
                "right": "Cat ipsum 1",
            },
        },
    }
    response = json.loads(self._post(data).data)[0]
    programs = response.get("Program")
    self.assertIsNot(programs, None)
    self.assertEqual(programs["count"], 1)
    self.assertEqual(len(programs["values"]), 1)
    self.assertEqual(programs["values"][0]["title"], "Cat ipsum 1")

    data = {
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "~"},
                "right": "1",
            },
        },
    }
    response = json.loads(self._post(data).data)[0]
    programs = response.get("Program")
    self.assertIsNot(programs, None)
    self.assertEqual(programs["count"], 12)
    self.assertEqual(len(programs["values"]), 12)

  @SkipTest
  def test_basic_query(self):
    pass

  @SkipTest
  def test_basic_query_filter(self):
    pass

  def test_basic_query_pagination(self):
    """Test basic query with pagination info."""
    from_, to_ = 1, 12
    data = {
        "object_name": "Program",
        "order_by": [{
            "name": "title",
        }],
        "limit": [from_, to_],
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "~"},
                "right": "Cat ipsum",
            },
        },
    }
    response = json.loads(self._post(data).data)[0]
    programs = response.get("Program")
    self.assertIsNot(programs, None)
    self.assertEqual(programs["count"], to_ - from_)
    self.assertEqual(len(programs["values"]), programs["count"])
    self.assertEqual(programs["total"], 23)

  def test_basic_query_total(self):
    """The value of "total" doesn't depend on "limit" parameter."""
    data_no_limit = {
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "~"},
                "right": "Cat ipsum",
            },
        },
    }
    response_no_limit = json.loads(self._post(data_no_limit).data)[0]
    programs_no_limit = response_no_limit.get("Program")
    self.assertIsNot(programs_no_limit, None)
    self.assertEqual(programs_no_limit["count"], programs_no_limit["total"])

    from_, to_ = 3, 5
    data_limit = data_no_limit.copy()
    data_limit.update({
        "limit": [from_, to_],
    })
    response_limit = json.loads(self._post(data_limit).data)[0]
    programs_limit = response_limit.get("Program")
    self.assertIsNot(programs_limit, None)
    self.assertEqual(programs_limit["count"], to_ - from_)

    self.assertEqual(programs_limit["total"], programs_no_limit["total"])

  @SkipTest
  def test_mapped_query(self):
    pass

  @SkipTest
  def test_mapped_query_filter(self):
    pass

  @SkipTest
  def test_mapped_query_pagination(self):
    pass

  @SkipTest
  def test_self_link(self):
    # It would be good if the api accepted get requests and we could add the
    # query into a get parameter, then each request would also get a self link
    # that could be tested to see that it truly returns what the original
    # request was.
    # In the end, instead of returning mapped object stubs like we do now, we'd
    # just return a self link for fetching those objects.
    pass
