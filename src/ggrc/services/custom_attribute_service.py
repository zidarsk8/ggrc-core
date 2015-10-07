# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: laran@reciprocitylabs.com
# Maintained By: laran@reciprocitylabs.com

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
