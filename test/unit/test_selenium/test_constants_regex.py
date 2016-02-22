# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Module for testing constant regex expressions."""

import re
from lib.constants import regex


def test_url_to_widget_info_regex():
  """Test regex for getting id and widget name from url."""
  urls = [
      ("https://grc-test.appspot.com/dashboard",
          "", ""),
      ("https://grc-test.appspot.com/dashboard#clause_widget",
          "", "clause_widget"),
      ("https://grc-test.appspot.com/clauses/90#/clause/90",
          90, "info_widget"),
      ("https://grc-test.appspot.com/clauses/90#",
          90, "info_widget"),
      ("https://grc-test.appspot.com/clauses/90",
          90, "info_widget"),
      ("https://grc-test.appspot.com/clauses/90#control_widget",
          90, "control_widget"),
      ("https://grc-test.appspot.com/clauses/90#info_widget",
          90, "info_widget"),
      ("https://grc-test.appspot.com/workflows/107",
          107, "info_widget"),
      ("https://grc-test.appspot.com/workflows/107#task_group_widget/"
          "task_group/122", 107, "task_group_widget"),
      ("https://grc-test.appspot.com/workflows/107#info_widget/workflow/107",
          107, "info_widget"),
      ("https://grc-test.appspot.com/workflows/107#/workflow/107",
          107, "info_widget"),
  ]

  for url, expected_id, expected_name in urls:
    object_id, name = re.match(regex.URL_WIDGET_INFO, url).groups()
    if object_id:
      object_id = int(object_id)
      name = name or "info_widget"

    assert object_id == expected_id
    assert name == expected_name
