# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for PUT and POST requests for objects with custom attributes

These tests include:
- Creating an object with custom attributes (POST request).
- Editing existing custom attributes on an object.
- Adding custom attributes to existing object.

"""


from ggrc import utils
from ggrc import models
from ggrc import builder

from integration.ggrc import services
from integration.ggrc.generator import ObjectGenerator


class TestGlobalCustomAttributes(services.TestCase):

  def setUp(self):
    services.TestCase.setUp(self)
    self.generator = ObjectGenerator()
    self.client.get("/login")

  def _post(self, data):
    return self.client.post(
        "/api/products",
        content_type='application/json',
        data=utils.as_json(data),
        headers={'X-Requested-By': 'Unit Tests'},
    )

  def test_custom_attribute_post(self):
    gen = self.generator.generate_custom_attribute
    _, cad = gen("product", attribute_type="Text", title="normal text")
    cad_json = builder.json.publish(cad.__class__.query.get(cad.id))
    cad_json = builder.json.publish_representation(cad_json)
    pid = models.Person.query.first().id

    product_data = [
        {
            "product": {
                "kind": None,
                "owners": [],
                "custom_attribute_values": [{
                  "attribute_value": "my custom attribute value",
                  "custom_attribute_id": cad.id,
                }],
                "contact": {
                    "id": pid,
                    "href": "/api/people/{}".format(pid),
                    "type": "Person"
                },
                "title": "simple product",
                "description": "",
                "secondary_contact": None,
                "notes": "",
                "url": "",
                "reference_url": "",
                "slug": "",
                "context": None
            }
        }
    ]

    response = self._post(product_data)
    import ipdb; ipdb.set_trace()

    product = models.Product.eager_query().first()
    self.assertEqual(len(product.custom_attribute_values), 1)
    self.assertEqual(
      product.custom_attribute_values[0].attribute_value,
      "my custom attribute value"
    )
