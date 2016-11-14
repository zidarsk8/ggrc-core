# coding: utf-8

# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for /query api endpoint."""


from ggrc import views
from ggrc import models

from integration.ggrc.converters import TestCase
from integration.ggrc.models import factories


class BaseQueryAPITestCase(TestCase):
  """Base class for /query api tests with utility methods."""

  def setUp(self):
    """Log in before performing queries."""
    super(BaseQueryAPITestCase, self).setUp()
    self.client.get("/login")

  def _setup_objects(self):
    text_cad = factories.CustomAttributeDefinitionFactory(
        definition_type="market",
    )
    date_cad = factories.CustomAttributeDefinitionFactory(
        definition_type="market",
        attribute_type="Text",
    )
    audit = factories.AuditFactory()
    for i in range(5):
      market = factories.MarketFactory()
      factories.CustomAttributeValueFactory(
          custom_attribute=date_cad,
          attributable=market,
          attribute_value="2016-11-0{}".format(i + 1),
      )
      factories.CustomAttributeValueFactory(
          custom_attribute=text_cad,
          attributable=market,
          attribute_value="2016-11-0{}".format(i + 1),
      )

    revisions = models.Revision.query.filter(
        models.Revision.resource_type == "Market")

    self.snapshots = [
        factories.SnapshotFactory(
            child_id=revision.resource_id,
            child_type=revision.resource_type,
            revision=revision,
            parent=audit,
        )
        for revision in revisions
    ]
    views.do_reindex()

  def test_basic_query_in(self):
    """Filter by ~ operator."""
    self._setup_objects()
