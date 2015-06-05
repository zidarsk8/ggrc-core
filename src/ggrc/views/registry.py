# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

from collections import namedtuple
from ggrc.views.common import BaseObjectView


ObjectViewEntry = namedtuple(
    'ObjectViewEntry', 'url model_class service_class')


def object_view(model_class, service_class=BaseObjectView):
  return ObjectViewEntry(
      model_class._inflector.table_plural,
      model_class,
      service_class)
