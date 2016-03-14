# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

"""Check number of db queries per API request.

This is in converters because it depends on import to provide data
"""

import sqlalchemy

from ggrc.models import all_models
from ggrc.views import all_object_views

from integration.ggrc.converters import TestCase
from integration.ggrc.generator import ObjectGenerator


# pylint: disable=too-few-public-methods
# because this is a small context manager
class QueryCounter(object):
  """Context manager for counting sqlalchemy database queries.

  Usage:
    with QueryCounter() as counter:
      query_count = counter.get
  """

  def __init__(self):
    self.counter = 0

    def after_cursor_execute(*_):
      self.counter += 1

    self.listener = after_cursor_execute

  def __enter__(self):
    sqlalchemy.event.listen(sqlalchemy.engine.Engine,
                            "after_cursor_execute",
                            self.listener)
    return self

  def __exit__(self, *_):
    sqlalchemy.event.remove(sqlalchemy.engine.Engine,
                            "after_cursor_execute",
                            self.listener)

  @property
  def get(self):
    return self.counter


class TestComprehensiveSheets(TestCase):

  """
  test sheet from:
    https://docs.google.com/spreadsheets/d/1Jg8jum2eQfvR3kZNVYbVKizWIGZXvfqv3yQpo2rIiD8/edit#gid=0

  """

  # skip abstract models since they are not really first class
  WHITELIST = {"Directive", "SystemOrProcess"}
  MODELS = [getattr(all_models, model_name)
            for model_name in all_models.__all__
            if model_name not in WHITELIST]

  def setUp(self):
    TestCase.setUp(self)
    self.generator = ObjectGenerator()
    self.client.get("/login")

    self.create_custom_attributes()
    self.create_people()
    filename = "comprehensive_sheet1.csv"
    self.import_file(filename)

  def tearDown(self):
    pass

  def test_queries_per_api_call(self):
    """Import comprehensive_sheet1 and count db requests per collection get.

    Query count should be <100 for all model types.
    """
    with QueryCounter() as counter:
      for model in self.MODELS:
        before = counter.counter
        self.generator.api.get_query(model, "")
        query_count = counter.get - before
        self.assertLess(query_count, 100,
                        "Query count for API GET" + model.__name__)

  def test_queries_per_object_page(self):
    """Import comprehensive_sheet1 and count db requests per collection get.

    Query count should be <100 for all model types.
    """
    with QueryCounter() as counter:
      for view in all_object_views():
        model = view.model_class
        if model not in self.MODELS:
          continue
        instance = model.query.first()
        if instance is None or getattr(instance, "id", None) is None:
          continue
        before = counter.counter
        res = self.client.get("/{}/{}".format(view.url, instance.id))
        self.assertEqual(res.status_code, 200)
        query_count = counter.counter - before
        self.assertLess(query_count, 100,
                        "Query count for object page " + model.__name__)

  def test_queries_for_dashboard(self):
    with QueryCounter() as counter:
      res = self.client.get("/permissions")
      self.assertEqual(res.status_code, 200)
      self.assertLess(counter.get, 100, "Query count for dashboard")

  def test_queries_for_permissions(self):
    with QueryCounter() as counter:
      res = self.client.get("/dashboard")
      self.assertEqual(res.status_code, 200)
      self.assertLess(counter.get, 100, "Query count for permissions")

  def create_custom_attributes(self):
    """Generate custom attributes needed by comprehensive_sheet1.csv."""
    gen = self.generator.generate_custom_attribute
    gen("control", title="my custom text", mandatory=True)
    gen("program", title="my_text", mandatory=True)
    gen("program", title="my_date", attribute_type="Date")
    gen("program", title="my_checkbox", attribute_type="Checkbox")
    gen("program", title="my_dropdown", attribute_type="Dropdown",
        options="a,b,c,d")

  def create_people(self):
    """Generate people needed by comprehensive_sheet1.csv."""
    emails = [
        "user1@ggrc.com",
        "miha@policy.com",
        "someone.else@ggrc.com",
        "another@user.com",
    ]
    for email in emails:
      self.generator.generate_person({
          "name": email.split("@")[0].title(),
          "email": email,
      }, "gGRC Admin")
