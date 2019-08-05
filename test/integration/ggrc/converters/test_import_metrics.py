# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for task group task specific export."""
from collections import OrderedDict

import ddt
import mock

from integration.ggrc import TestCase
from integration.ggrc.models import factories
from ggrc.converters import errors
from ggrc.models import all_models


@ddt.ddt
class TestMetricsImport(TestCase):
  """Test for metrics import."""

  def setUp(self):
    super(TestMetricsImport, self).setUp()
    self.client.get("/login")

  def test_metrics_import(self):
    """Test metrics import"""
    filename = "import_metrics.csv"
    response = self._import_file(filename)
    metric_response = response[2]
    self.assertEqual(metric_response["created"], 3)
    self._check_csv_response(response, {
        "Metric": {
            "row_warnings": {
                errors.MAPPING_SCOPING_ERROR.format(
                    line=14,
                    object_type="Regulation",
                    action="map",
                ),
                errors.MAPPING_SCOPING_ERROR.format(
                    line=15,
                    object_type="Standard",
                    action="map",
                ),
            },
        }
    })

  @ddt.data(
      (True, "test_ggrcq"),
      (False, ""),
  )
  @ddt.unpack
  def test_metrics_deprecated_import(self, is_integration, test_url):
    """Test metrics import with Deprecated status message"""
    with mock.patch("ggrc.settings.GGRC_Q_INTEGRATION_URL",
                    test_url) as ggrc_q_link:
      metric = factories.MetricFactory()
      self.assertEqual(metric.status, "Draft")
      response = self.import_data(OrderedDict([
          ("object_type", "Metric"),
          ("Code*", metric.slug),
          ("Launch Status", "Deprecated"),
      ]))
      expected_response = {} if not is_integration else {
          "Metric": {
              "row_warnings": {
                  errors.DEPRECATED_DELETED_METRIC_STATUS.format(
                      line=3,
                      object_type="Metric",
                      object_title=metric.title,
                      ggrc_q_link=ggrc_q_link,
                      action_status="deprecation",
                  ),
              },
          }
      }
      self._check_csv_response(response, expected_response)
      metric = all_models.Metric.query.first()
      self.assertEqual(metric.status, "Deprecated")
