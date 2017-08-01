# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Unit tests for Assessment summary query handler."""

import unittest
import ddt

from ggrc.query import assessments_summary_handler


@ddt.ddt
class TestAssessmentSummarHandler(unittest.TestCase):
  """Unit tests for Assessment summary query handler."""

  @ddt.data(
      [],
      [{}, {}, {}],
      [{  # contains order by title
          "object_name": "Assessment",
          "filters": {
              "expression": {
                  "object_name": "Audit",
                  "op": {"name": "relevant"},
                  "ids": ["347"]},
              "keys":[],
              "order_by":{"keys": [], "order":"title", "compare":None}},
          "fields":["status", "verified"],
      }],
      [{  # invalid requested fields
          "object_name": "Assessment",
          "filters": {
              "expression": {
                  "object_name": "Audit",
                  "op": {"name": "relevant"},
                  "ids": ["347"]},
              "keys":[],
              "order_by":{"keys": [], "order":"", "compare":None}},
          "fields":["status"],
      }],
      [{  # too many Audit ids
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
      }],
      [{  # missing audit ids
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
      }],
  )
  def test_not_matching(self, data):
    handler = assessments_summary_handler.AssessmentsSummaryHandler
    self.assertFalse(handler.match(data))

  @ddt.data(
      [{  # normal request
          "object_name": "Assessment",
          "filters": {
              "expression": {
                  "object_name": "Audit",
                  "op": {"name": "relevant"},
                  "ids": ["347"]},
              "keys":[],
              "order_by":{"keys": [], "order":"", "compare":None}},
          "fields":["status", "verified"],
      }],
      [{  # with query type filed
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
      }],
  )
  def test_matching(self, data):
    handler = assessments_summary_handler.AssessmentsSummaryHandler
    self.assertTrue(handler.match(data))
