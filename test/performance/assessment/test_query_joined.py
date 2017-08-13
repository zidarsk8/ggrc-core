# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for locust read tasks."""

import logging
import random

import locust

from performance import base
from performance import generator

random.seed(1)


logger = logging.getLogger()


class AssessmentTest(base.BaseTaskSet):
  """Tests for assessment read operations."""

  @locust.task(1)
  def joined_related_query(self):
    """Get all objects related to an assessment in a single request."""
    assessment = generator.random_object("Assessment", self.objects)
    assessment_id = str(assessment["id"])

    query = [{
        "object_name": "Snapshot",
        "filters": {
            "expression": {
             "object_name": "Assessment",
             "op": {"name": "relevant"},
             "ids": [assessment_id]
             },
            "keys":[],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "fields":[]
    }, {
        "object_name": "Comment",
        "filters": {
            "expression": {
                "object_name": "Assessment",
                "op": {"name": "relevant"},
                "ids": [assessment_id]
            },
            "keys":[],
            "order_by":{"keys": [], "order":"", "compare":None}
        },
        "order_by":[{"name": "created_at", "desc": True}],
        "fields": []
    }, {
        "object_name": "Document",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": [assessment_id]
                },
                "op":{"name": "AND"},
                "right": {
                    "left": "document_type",
                    "op": {"name": "="},
                    "right": "EVIDENCE"
                }
            },
            "keys": [None]
        },
        "order_by":[{"name": "created_at", "desc": True}],
        "fields": []
    }, {
        "object_name": "Document",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": [assessment_id]
                },
                "op":{"name": "AND"},
                "right": {
                    "left": "document_type",
                    "op": {"name": "="},
                    "right": "URL"
                }
            },
            "keys": [None]
        },
        "order_by":[{"name": "created_at", "desc": True}],
        "fields": []
    }, {
        "object_name": "Document",
        "filters": {
            "expression": {
                "left": {
                    "object_name": "Assessment",
                    "op": {"name": "relevant"},
                    "ids": [assessment_id]
                },
                "op":{"name": "AND"},
                "right": {
                    "left": "document_type",
                    "op": {"name": "="},
                    "right": "REFERENCE_URL"
                }
            },
            "keys": [None]
        },
        "fields":[],
        "order_by":[{"name": "created_at", "desc": True}]
        # }, {
        #     "object_name": "Audit",
        #     "filters": {
        #         "expression": {
        #             "object_name": "Assessment",
        #             "op": {"name": "relevant"},
        #             "ids": [assessment_id]
        #         },
        #         "keys":[],
        #         "order_by":{"keys": [], "order":"", "compare":None}
        #     },
        #     "limit":[0, 1],
        #     "fields":["id", "type", "title", "context"]
    }]
    self.client.post(
        "/query",
        headers=self.headers,
        json=query,
        name="/query joined",
    )


class WebsiteUser(locust.HttpLocust):
  """Locust http task runner."""
  # pylint: disable=too-few-public-methods
  task_set = AssessmentTest
  min_wait = 1000
  max_wait = 1000
