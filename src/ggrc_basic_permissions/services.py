# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from ggrc.services.common import Resource

class PermissionsResource(Resource):
  def get_collection(self, filter_by_contexts=False):
    # These resources are special and ALWAYS require admin, regardless of
    # context... this may change later so that you can have a context admin...
    # or... this could really be covered by permissions... 
    return super(PermissionsResource, self)\
        .get_collection(filter_by_contexts=False)

