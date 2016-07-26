# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Base test case for all ggrc integration tests."""

import logging
from sqlalchemy import exc
from flask.ext.testing import TestCase as BaseTestCase
from ggrc import db
from ggrc.app import app

# Hide errors during testing. Errors are still displayed after all tests are
# done. This is for the bad request error messages while testing the api calls.
logging.disable(logging.CRITICAL)


class TestCase(BaseTestCase):
  # pylint: disable=invalid-name
  # because it's required by unittests.

  """Base test case for all ggrc integration tests."""

  maxDiff = None

  @classmethod
  def clear_data(cls):
    """Remove data from ggrc tables.

    This is a helper function to remove any data that might have been generated
    during a test. The ignored tables are the ones that don't exist or have
    constant data in them, that was populated with migrations.


    Note:
      This is a hack because db.metadata.sorted_tables does not sort by
      dependencies. The events table is given before Person table and reversed
      order in then incorrect.
    """
    ignore_tables = (
        "categories",
        "notification_types",
        "object_types",
        "options",
        "relationship_test_mock_model",
        "roles",
        "test_model",
    )
    tables = set(db.metadata.tables).difference(ignore_tables)
    for _ in range(len(tables)):
      if len(tables) == 0:
        break  # stop the loop once all tables have been deleted
      for table in reversed(db.metadata.sorted_tables):
        if table.name in tables:
          try:
            db.engine.execute(table.delete())
            tables.remove(table.name)
          except exc.IntegrityError:
            pass

    db.session.commit()

  def setUp(self):
    self.clear_data()

  def tearDown(self):  # pylint: disable=no-self-use
    db.session.remove()

  @staticmethod
  def create_app():
    """Flask specific function for running an app instance."""
    app.config["SERVER_NAME"] = "localhost"
    app.testing = True
    app.debug = False
    return app

  def _check_response(self, response, expected_errors):
    """Test that response contains all expected errors and warnigs.

    Args:
      response: api response object.
      expected_errors: dict of all expected errors by object type.

    Raises:
      AssertionError if an expected error or warning is not found in the
        proper response block.
    """

    messages = ("block_errors", "block_warnings", "row_errors", "row_warnings")

    for block in response:
      for message in messages:
        expected = expected_errors.get(block["name"], {}).get(message, set())
        self.assertEqual(set(expected), set(block[message]))
