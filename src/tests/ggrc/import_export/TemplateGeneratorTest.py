import ggrc
from ggrc import db
from tests.ggrc import TestCase
from ggrc.services.custom_attribute_service import CustomAttributeService
from ggrc.models import CustomAttributeDefinition, CustomAttributeValue
import unittest

class TemplateGeneratorTest(TestCase):

  def test_get_attributes_for_type(self):

    definition = CustomAttributeDefinition(
      title = 'Test Control Attribute Definition',
      definition_type = 'Control',
      attribute_type = CustomAttributeDefinition.ValidTypes.TEXT,
      mandatory = False,
      helptext = 'Don\'t eat the yellow snow.',
      placeholder = 'A placeholder'
    )
    db.session.add(definition)
    db.session.commit()
    db.session.flush()

    //

    model_type = 'Control'
    _model = ggrc.models.get_model(model_type)
    published_attributes = _model._publish_attrs
    custom_attribute_definitions    = \
      CustomAttributeService.attribute_definitions_for_type(model_type)

    self.assertEqual(1, len(custom_attribute_definitions))

    print "published_attributes: {a}".format(a=published_attributes)
    print "custom_attribute_definitions: {a}".format(a=custom_attribute_definitions)

    db.session.delete(definition)

if __name__ == '__main__':
    unittest.main()