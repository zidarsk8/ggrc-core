# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Service descriptor."""

from cached_property import cached_property

from docbuilder.descriptors.base import Descriptor
from docbuilder.descriptors.model import Model


class Service(Descriptor):
  """Service descriptor."""

  @classmethod
  def collect(cls):
    """Collects all application services."""
    from ggrc.services import all_services

    return all_services()

  @cached_property
  def name(self):
    """Service name."""
    return '%s -> %s' % (self.model.name, self.obj.name)

  @cached_property
  def url(self):
    """Endpoint URL."""
    return '/api/%s' % self.obj.name

  @cached_property
  def doc(self):
    """Doc-stirng of wrapped model class."""
    return self.model.doc

  @cached_property
  def model(self):
    """Descriptor of wrapped model class."""
    return Model(self.obj.model_class)

  @cached_property
  def readonly(self):
    """Is service read-only?"""
    return self.obj.service_class.__name__.startswith('ReadOnly')
