# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc import db
from ggrc.models import CustomAttributeDefinition
from ggrc.utils import underscore_from_camelcase


class CustomAttributeService(object):

  """

  """
  @staticmethod
  def attribute_definitions_for_type(ttype):
    return db.session.query(CustomAttributeDefinition)\
      .filter(CustomAttributeDefinition.definition_type ==
              underscore_from_camelcase(ttype))\
      .order_by(CustomAttributeDefinition.title)\
      .all()
