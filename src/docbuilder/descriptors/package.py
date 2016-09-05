# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

import sys

from cached_property import cached_property

from docbuilder.descriptors.base import Descriptor
from docbuilder.descriptors.service import Service
from docbuilder.descriptors.model import Model, Mixin


class Package(Descriptor):

  @classmethod
  def collect(cls):
    from ggrc import app
    app = app

    for name, module in sys.modules.iteritems():
      if name.startswith('ggrc') and '.' not in name:
        yield module

  @cached_property
  def services(self):
    return self._descriptors(Service)

  @cached_property
  def models(self):
    return self._descriptors(Model)

  @cached_property
  def mixins(self):
    return self._descriptors(Mixin)

  def _descriptors(self, class_):
    prefix = self.name + '.'
    return [
        descriptor
        for descriptor in class_.all()
        if descriptor.name.startswith(prefix)
    ]
