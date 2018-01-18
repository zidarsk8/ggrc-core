# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Custom Resource for Relationship that creates Snapshots when needed.

When Audit-Snapshottable Relationship is POSTed, a Snapshot should be created
instead.
"""

from werkzeug.exceptions import BadRequest, Forbidden
from flask import request

from ggrc import db
from ggrc import models
from ggrc import login
from ggrc.utils import benchmark
from ggrc.rbac import permissions
from ggrc.services import common


class RelatedAssessmentsResource(common.ExtendedResource):
  """Resource handler for audits."""



  @classmethod
  def add_to(cls, app, url, model_class=None, decorators=()):
    view_func = cls.as_view(cls.endpoint_name())
    app.add_url_rule(
        '{url}/<string:object_type>/<int:object_id>/'
        '<int:first>/<int:last>'.format(url=url),
        view_func=view_func,
        methods=['GET']
    )
    app.add_url_rule(
        '{url}/<string:object_type>/<int:object_id>'.format(url=url),
        view_func=view_func,
        methods=['GET']
    )

  def dispatch_request(self, *args, **kwargs):  # noqa
    """Dispatch request for related_assessments."""

    object_type = kwargs.pop("object_type")
    object_id = kwargs.pop("object_id")

    if request.method != 'GET':
      raise BadRequest()
    if not permissions.is_allowed_read(object_id, object_type, None):
      raise Forbidden()

    model = models.inflector.get_model(object_type)

    ids_query = model.get_similar_objects_query(object_id, "Assessment")
    return self.json_success_response({'OK': 1}, )
