# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""This module contains special query helper class for query API."""

import copy

from werkzeug.exceptions import Forbidden
from cached_property import cached_property

from ggrc import db
from ggrc import models
from ggrc.utils import benchmark
from ggrc.rbac import permissions
from ggrc.query.default_handler import DefaultHandler


# pylint: disable=too-few-public-methods

class AssessmentsSummaryHandler(DefaultHandler):
  """Handler for assessment filter on my assessments page.

  Query filters with single relevant person and assessment statuses.

  """

  @classmethod
  def match(cls, query):
    """Check if the given query matches current handler."""
    if len(query) != 1:
      return False
    query = copy.deepcopy(query[0])
    audit_ids = query["filters"]["expression"]["ids"]
    if not isinstance(audit_ids, list) or len(audit_ids) != 1:
      return False
    query_type = query.pop("type", "values")
    if query_type != "values":
      return False
    expected = {
        "object_name": "Assessment",
        "filters": {
            "expression": {
                "object_name": "Audit",
                "op": {"name": "relevant"},
                "ids": audit_ids},
            "keys": [],
            "order_by": {"keys": [], "order": "", "compare": None}},
        "fields": ["status", "verified"]
    }
    if query != expected:
      return False
    return True

  @cached_property
  def _audit(self):
    """Get the audit used in the query and verify its permissions."""
    audit_id = self.query[0]["filters"]["expression"]["ids"][0]
    audit = models.Audit.query.get(audit_id)
    if permissions.is_allowed_read_for(audit):
      return audit
    raise Forbidden()

  def get_results(self):
    """Filter the objects and get their information.

    Updates self.query items with their results. The type of results required
    is read from "type" parameter of every object_query in self.query.

    Returns:
      list of dicts: same query as the input with requested results that match
                     the filter.
    """
    object_query = self.query[0]

    with benchmark("Get Assessment statuses"):
      data = db.session.query(
          models.Assessment.status,
          models.Assessment.verified,
      ).filter(
          models.Assessment.audit_id == self._audit.id
      ).all()
    with benchmark("serialization: get_results > _transform_to_json"):
      object_query["count"] = len(data)
      object_query["total"] = len(data)
      object_query["last_modified"] = None
      object_query["values"] = [
          {"status": status, "verified": bool(verified)}
          for status, verified in data
      ]
    return self.query
