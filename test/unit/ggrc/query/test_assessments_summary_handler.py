# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Unit tests for Assessment summary query handler."""

import unittest
import ddt

from ggrc.query import assessments_summary_handler


class TestQueries(object):
  """Test data for matcher for assessment query handler."""
  # pylint: disable=too-few-public-methods

  NO_QUERIES = []

  MULTIPLE_EMPTY = [{}, {}, {}]

  ORDER_BY_TITLE = [{
      "object_name": "Assessment",
      "filters": {
          "expression": {
              "object_name": "Audit",
              "op": {"name": "relevant"},
              "ids": ["347"]},
          "keys":[],
          "order_by":{"keys": [], "order":"title", "compare":None}},
      "fields":["status", "verified"],
  }]

  INVALID_REQUESTED_FIELDS = [{
      "object_name": "Assessment",
      "filters": {
          "expression": {
              "object_name": "Audit",
              "op": {"name": "relevant"},
              "ids": ["347"]},
          "keys":[],
          "order_by":{"keys": [], "order":"", "compare":None}},
      "fields":["status"],
  }]

  TOO_MANY_AUDIT_IDS = [{
      "object_name": "Assessment",
      "filters": {
          "expression": {
              "object_name": "Audit",
              "op": {"name": "relevant"},
              "ids": ["1", "2", "55"]},
          "keys":[],
          "order_by":{"keys": [], "order":"", "compare":None}},
      "fields":["status", "verified"],
      "type": "values",
  }]

  MISSING_AUDIT_IDS = [{
      "object_name": "Assessment",
      "filters": {
          "expression": {
              "object_name": "Audit",
              "op": {"name": "relevant"},
              "ids": []},
          "keys":[],
          "order_by":{"keys": [], "order":"", "compare":None}},
      "fields":["status", "verified"],
      "type": "values",
  }]

  NORMAL_REQUEST = [{
      "object_name": "Assessment",
      "filters": {
          "expression": {
              "object_name": "Audit",
              "op": {"name": "relevant"},
              "ids": ["347"]},
          "keys":[],
          "order_by":{"keys": [], "order":"", "compare":None}},
      "fields":["status", "verified"],
  }]

  WITH_QUERY_TYPE_FIELD = [{
      "object_name": "Assessment",
      "filters": {
          "expression": {
              "object_name": "Audit",
              "op": {"name": "relevant"},
              "ids": ["347"]},
          "keys":[],
          "order_by":{"keys": [], "order":"", "compare":None}},
      "fields":["status", "verified"],
      "type": "values",
  }]


@ddt.ddt
class TestAssessmentSummarHandler(unittest.TestCase):
  """Unit tests for Assessment summary query handler."""

  HANDLER = assessments_summary_handler.AssessmentsSummaryHandler

  @ddt.data(
      (False, TestQueries.INVALID_REQUESTED_FIELDS),
      (False, TestQueries.MISSING_AUDIT_IDS),
      (False, TestQueries.MULTIPLE_EMPTY),
      (False, TestQueries.NO_QUERIES),
      (False, TestQueries.ORDER_BY_TITLE),
      (False, TestQueries.TOO_MANY_AUDIT_IDS),
      (True, TestQueries.NORMAL_REQUEST),
      (True, TestQueries.WITH_QUERY_TYPE_FIELD),
  )
  @ddt.unpack
  def test_not_matching(self, match, data):
    self.assertIs(match, self.HANDLER.match(data))
