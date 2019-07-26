# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for task group task specific export."""
from collections import OrderedDict

from integration.ggrc import TestCase
from integration.ggrc.models import factories
from ggrc.converters import errors
from ggrc.models import all_models


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

  def test_metrics_deprecated_import(self):
    """Test metrics import with Deprecated status message"""
    from ggrc.settings import default

    metric = factories.MetricFactory()
    self.assertEqual(metric.status, "Draft")
    response = self.import_data(OrderedDict([
        ("object_type", "Metric"),
        ("Code*", metric.slug),
        ("Launch Status", "Deprecated"),
    ]))
    self._check_csv_response(response, {
        "Metric": {
            "row_warnings": {
                errors.DEPRECATED_METRIC_STATUS.format(
                    line=3,
                    object_type="Metric",
                    object_title=metric.title,
                    ggrc_q_link=default.GGRC_Q_INTEGRATION_URL,
                ),
            },
        }
    })
    metric = all_models.Metric.query.first()
    self.assertEqual(metric.status, "Deprecated")
