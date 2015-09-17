# Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
# Unauthorized use, copying, distribution, displaying, or public performance
# of this file, via any medium, is strictly prohibited. All information
# contained herein is proprietary and confidential and may not be shared
# with any third party without the express written consent of Reciprocity, Inc.
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

import re

from ggrc import db
from ggrc.converters.base_row import LinksHandler
from ggrc_risks import _risk_object_types
from ggrc_risks.models import RiskObject


class RiskObjectsHandler(LinksHandler):

  def parse_item(self, value):
    """Will only return valid risk object classes
    """
    # check that it has the format type:slug
    # match on <start><not colons>:<not colons><end>
    match = re.match(r'^[^:]+:[^:]+$', value)
    if not match:
      self.add_link_error(u"Invalid format. Please use the following format: 'System:SYSTEM-001'.")
      return
    obj_type_str, slug = tuple([v.strip() for v in value.split(":")])
    if obj_type_str not in _risk_object_types:
      self.add_link_error(u"'{}' is not a valid type.".format(obj_type_str))
      return
    else:
      import ggrc.models
      obj_class = ggrc.models.__getattribute__(obj_type_str)
      return {'obj_class': obj_class, 'slug': slug}

  def export(self):
    obj = self.importer.obj
    mapped_objs = getattr(obj, self.key, [])
    # funcion for the pattern <object type>:<slug>
    def obj_string(o):
      return u"{0}:{1}".format(o.__class__.__name__, o.slug)
    return u"\n".join([obj_string(o) for o in mapped_objs])

  def create_item(self, data):
    if not data:
      return
    model_class = data.get('obj_class')
    self.add_link_warning(u"{} with code '{}' doesn't exist.".format(
      model_class.__name__, data.get('slug')))

  def find_existing_item(self, data):
    if not data:
      return None
    where_params = {'slug': data.get('slug')}
    model_class = data.get('obj_class')
    return model_class.query.filter_by(**where_params).first() or None

  def get_existing_items(self):
    objects = []
    where_params = {}
    where_params['risk_id'] = self.importer.obj.id
    risk_objects = RiskObject.query.filter_by(**where_params).all()
    return [risk_obj.object for risk_obj in risk_objects]

  def after_save(self, obj):
    for linked_object in self.created_links():
      db.session.add(linked_object)
      risk_object = RiskObject()
      risk_object.risk = self.importer.obj
      risk_object.object = linked_object
      db.session.add(risk_object)

