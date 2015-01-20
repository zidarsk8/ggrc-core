import ggrc

class TemplateGenerator(object):

  @staticmethod
  def template_for(model_type):
    _model = ggrc.models.get_model(model_type)
    published_attributes = _model.publish_attrs
    custom_attributes    = CustomAttributeService.attribute_definitions_for_type(model_type)


