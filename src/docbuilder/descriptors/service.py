# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from cached_property import cached_property

from docbuilder.descriptors.base import Descriptor
from docbuilder.descriptors.model import Model


class Service(Descriptor):

  @classmethod
  def collect(cls):
    from ggrc.services import all_services

    return all_services()

  @cached_property
  def name(self):
    return '%s -> %s' % (self.model.name, self.obj.name)

  @cached_property
  def url(self):
    return '/api/%s' % self.obj.name

  @cached_property
  def doc(self):
    return self.model.doc

  @cached_property
  def model(self):
    return Model(self.obj.model_class)

  @cached_property
  def readonly(self):
    return self.obj.service_class.__name__.startswith('ReadOnly')
