# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from cached_property import cached_property

from docbuilder.descriptors.base import Descriptor


class Model(Descriptor):

  @classmethod
  def collect(cls):
    from ggrc.models.all_models import all_models

    return all_models

  @cached_property
  def mixins(self):
    return [Mixin(class_) for class_ in _mixins(self.obj)]


class Mixin(Descriptor):

  @classmethod
  def collect(cls):
    result = set()
    for model in Model.all():
      result.update(_mixins(model.obj))
    return result


def _mixins(model_class):
  for class_ in model_class.mro()[1:]:
    if class_.__module__.startswith('ggrc'):
      yield class_
