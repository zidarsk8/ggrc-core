# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for /query api endpoint."""

from datetime import datetime
from os.path import abspath, dirname, join
from flask import json
from nose.plugins.skip import SkipTest

from ggrc.app import app
from integration.ggrc import TestCase


THIS_ABS_PATH = abspath(dirname(__file__))
CSV_DIR = join(THIS_ABS_PATH, '../converters/test_csvs/')

# to be moved into converters.query_helper
DATE_FORMAT_REQUEST = "%m/%d/%Y"
DATE_FORMAT_RESPONSE = "%Y-%m-%d"


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

  def test_basic_query_eq(self):
    """Filter by = operator."""
    title = "Cat ipsum 1"
    data = {
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "="},
                "right": title,
            },
        },
    }
    response = json.loads(self._post(data).data)[0]
    programs = response.get("Program")
    self.assertIsNot(programs, None)
    self.assertEqual(programs["count"], 1)
    self.assertEqual(len(programs["values"]), programs["count"])
    self.assertEqual(programs["values"][0]["title"], title)

  def test_basic_query_in(self):
    """Filter by ~ operator."""
    title_pattern = "1"
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
    self.assertEqual(len(programs["values"]), programs["count"])
    self.assertTrue(all(title_pattern in program["title"]
                        for program in programs["values"]))

  def test_basic_query_ne(self):
    """Filter by != operator."""
    title = "Cat ipsum 1"
    data = {
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "!="},
                "right": title,
            },
        },
    }
    response = json.loads(self._post(data).data)[0]
    programs = response.get("Program")
    self.assertIsNot(programs, None)
    self.assertEqual(programs["count"], 22)
    self.assertEqual(len(programs["values"]), programs["count"])
    self.assertTrue(all(program["title"] != title
                        for program in programs["values"]))

  def test_basic_query_not_in(self):
    """Filter by !~ operator."""
    title_pattern = "1"
    data = {
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "!~"},
                "right": title_pattern,
            },
        },
    }
    response = json.loads(self._post(data).data)[0]
    programs = response.get("Program")
    self.assertIsNot(programs, None)
    self.assertEqual(programs["count"], 11)
    self.assertEqual(len(programs["values"]), programs["count"])
    self.assertTrue(all(title_pattern not in program["title"]
                        for program in programs["values"]))

  def test_basic_query_lt(self):
    """Filter by < operator."""
    date = datetime(2015, 5, 18)
    data = {
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "effective date",
                "op": {"name": "<"},
                "right": date.strftime(DATE_FORMAT_REQUEST),
            },
        },
    }
    response = json.loads(self._post(data).data)[0]
    programs = response.get("Program")
    self.assertIsNot(programs, None)
    self.assertEqual(programs["count"], 9)
    self.assertEqual(len(programs["values"]), programs["count"])
    self.assertTrue(
        all(datetime.strptime(program["start_date"],
                              DATE_FORMAT_RESPONSE) < date
            for program in programs["values"]),
    )

  def test_basic_query_gt(self):
    """Filter by > operator."""
    date = datetime(2015, 5, 18)
    data = {
        "object_name": "Program",
        "filters": {
            "expression": {
                "left": "effective date",
                "op": {"name": ">"},
                "right": date.strftime(DATE_FORMAT_REQUEST),
            },
        },
    }
    response = json.loads(self._post(data).data)[0]
    programs = response.get("Program")
    self.assertIsNot(programs, None)
    self.assertEqual(programs["count"], 13)
    self.assertEqual(len(programs["values"]), programs["count"])
    self.assertTrue(
        all(datetime.strptime(program["start_date"],
                              DATE_FORMAT_RESPONSE) > date
            for program in programs["values"]),
    )

  def test_basic_query_text_search(self):
    """Filter by fulltext search."""
    text_pattern = "ea"
    data = {
        "object_name": "Regulation",
        "fields": ["description", "notes"],
        "filters": {
            "expression": {
                "op": {"name": "text_search"},
                "text": text_pattern,
            },
        },
    }
    response = json.loads(self._post(data).data)[0]
    regulations = response.get("Regulation")
    self.assertIsNot(regulations, None)
    self.assertEqual(regulations["count"], 21)
    self.assertEqual(len(regulations["values"]), regulations["count"])
    self.assertTrue(all((regulation["description"] and
                         text_pattern in regulation["description"]) or
                        (regulation["notes"] and
                         text_pattern in regulation.get("notes", ""))
                        for regulation in regulations["values"]))

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

  def test_query_count(self):
    """The value of "count" is same for "values" and "count" queries."""
    data_values = {
        "object_name": "Program",
        "type": "values",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "~"},
                "right": "Cat ipsum",
            },
        },
    }
    response_values = json.loads(self._post(data_values).data)[0]
    programs_values = response_values.get("Program")
    self.assertIsNot(programs_values, None)

    data_count = {
        "object_name": "Program",
        "type": "count",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "~"},
                "right": "Cat ipsum",
            },
        },
    }
    response_count = json.loads(self._post(data_count).data)[0]
    programs_count = response_count.get("Program")
    self.assertIsNot(programs_count, None)

    self.assertEqual(programs_values["count"], programs_count["count"])

  def test_query_ids(self):
    """The ids are the same for "values" and "ids" queries."""
    data_values = {
        "object_name": "Program",
        "type": "values",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "~"},
                "right": "Cat ipsum",
            },
        },
    }
    response_values = json.loads(self._post(data_values).data)[0]
    programs_values = response_values.get("Program")
    self.assertIsNot(programs_values, None)

    data_ids = {
        "object_name": "Program",
        "type": "ids",
        "filters": {
            "expression": {
                "left": "title",
                "op": {"name": "~"},
                "right": "Cat ipsum",
            },
        },
    }
    response_ids = json.loads(self._post(data_ids).data)[0]
    programs_ids = response_ids.get("Program")
    self.assertIsNot(programs_ids, None)

    self.assertEqual(
        set(obj.get("id") for obj in programs_values["values"]),
        set(programs_ids["ids"]),
    )

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
