# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for /api/relationship endpoints."""

import json

from integration.ggrc import api_helper
from integration.ggrc.models import factories
from integration.ggrc.services import TestCase


class TestRelationshipResource(TestCase):
  """Tests for special api endpoints."""

  def setUp(self):
    super(TestRelationshipResource, self).setUp()
    self.api = api_helper.Api()

  def test_map_object(self):
    """It should be possible to map an object to an audit."""
    with factories.single_commit():
      program = factories.ProgramFactory()
      audit = factories.AuditFactory(program=program)
      factories.RelationshipFactory(
          source=audit,
          destination=program
      )
      product = factories.ProductFactory()
      factories.RelationshipFactory(
          source=program,
          destination=product
      )

    data = [{
        "relationship": {
            "context": None,
            "destination": {
                "id": product.id,
                "type": "Product",
                "href": "/api/products/{}".format(product.id)
            },
            "source": {
                "id": audit.id,
                "type": "Audit",
                "href": "/api/audits/{}".format(audit.id)
            }
        }
    }]

    response = self.api.client.post(
        "/api/relationships",
        data=json.dumps(data),
        headers=self.headers
    )
    self.assert200(response)
