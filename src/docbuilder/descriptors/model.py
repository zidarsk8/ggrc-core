# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from cached_property import cached_property
from sqlalchemy.dialects import mysql
from sqlalchemy.schema import CreateTable

from docbuilder.descriptors.base import Descriptor


class Model(Descriptor):

  @classmethod
  def collect(cls):
    from ggrc.models.all_models import all_models

    return all_models

  @cached_property
  def mixins(self):
    return [
        Mixin(class_) for class_ in self.obj.mro()[1:]
        if class_.__module__.startswith('ggrc')
    ]

  @cached_property
  def create_table(self):
    query = CreateTable(self.obj.__table__).compile(dialect=mysql.dialect())
    return str(query).strip()


class Mixin(Descriptor):

  @classmethod
  def collect(cls):
    result = set()
    for model in Model.all():
      result.update(m.obj for m in model.mixins)
    return result
