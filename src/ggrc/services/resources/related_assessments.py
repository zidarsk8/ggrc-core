# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Custom resource for related assessments

This resource works with the following queries:
  - /api/related_assess with get parameters:
    - object_type=Control
    - object_id=XXX
    - optional: limit=from,to
    - optional: order_by=field_name[,asc|,desc]
"""

from collections import defaultdict

from werkzeug.exceptions import BadRequest, Forbidden
from flask import request

from sqlalchemy import orm
from sqlalchemy import and_

from ggrc import db
from ggrc import models
from ggrc.utils import benchmark
from ggrc.rbac import permissions
from ggrc.services import common
from ggrc.query import pagination
from ggrc.query.exceptions import BadQueryException


class RelatedAssessmentsResource(common.Resource):
  """Resource handler for audits."""

  @classmethod
  def add_to(cls, app, url, model_class=None, decorators=()):
    view_func = cls.as_view(cls.endpoint_name())
    app.add_url_rule(url, view_func=view_func, methods=['GET'])

  def _get_assessments(self, model, object_type, object_id, order_by, limit):

    ids_query = model.get_similar_objects_query(object_id, "Assessment")

    if not permissions.has_system_wide_read():
      if not permissions.is_allowed_read(object_id, object_type, None):
        raise Forbidden()
      acl = models.all_models.AccessControlList
      acr = models.all_models.AccessControlRole
      ids_query = db.session.query(acl.object_id).join(acr).filter(
          acr.read.is_(True),
          acl.object_type == "Assessment",
          acl.object_id.in_(ids_query)
      )

    query = models.Assessment.query.options(
        orm.Load(models.Assessment).undefer_group(
            "Assessment_complete",
        ),
        orm.Load(models.Assessment).joinedload(
            "audit"
        ).undefer_group(
            "Audit_complete",
        ),
        orm.Load(models.Assessment).joinedload(
            "custom_attribute_definitions"
        ).undefer_group(
            "CustomAttributeDefinitons_complete",
        ),
        orm.Load(models.Assessment).joinedload(
            "custom_attribute_values"
        ).undefer_group(
            "CustomAttributeValues_complete",
        ),
    ).filter(
        models.Assessment.id.in_(ids_query)
    )
    if order_by:
      query = pagination.apply_order_by(
          models.Assessment,
          query,
          order_by,
          models.Assessment,
      )
    if limit:
      limit_query, total = pagination.apply_limit(query, limit)

    return limit_query, total

  def _get_documents(self, assessments):

    assessment_ids = [asmt.id for asmt in assessments]

    related_document_types = (
        models.Document.ATTACHMENT,
        models.Document.URL,
    )

    source_query = db.session.query(
        models.Relationship.destination_id.label("assessment_id"),
        models.Relationship.source_id.label("document_id")
    ).join(
        models.Document,
        and_(
            models.Relationship.source_type == models.Document.__name__,
            models.Relationship.source_id == models.Document.id
        )
    ).filter(
        models.Relationship.destination_id.in_(assessment_ids),
        models.Relationship.destination_type == models.Assessment.__name__,
        models.Document.document_type.in_(related_document_types)
    )

    destination_query = db.session.query(
        models.Relationship.source_id.label("assessment_id"),
        models.Relationship.destination_id.label("snapshot_id")
    ).join(
        models.Document,
        and_(
            models.Relationship.destination_type == models.Document.__name__,
            models.Relationship.destination_id == models.Document.id
        )
    ).filter(
        models.Relationship.source_id.in_(assessment_ids),
        models.Relationship.source_type == models.Assessment.__name__,
        models.Document.document_type.in_(related_document_types)
    )

    assessment_document_map = defaultdict(set)
    all_document_ids = set()
    for assessment_id, document_id in source_query.union(destination_query):
      assessment_document_map[assessment_id].add(document_id)
      all_document_ids.add(document_id)

    if all_document_ids:
      documents = models.Document.query.options(
          orm.Load(models.Document).undefer_group("Document_complete")
      ).filter(
          models.Document.id.in_(all_document_ids)
      ).all()

      documents_map = {document.id: document for document in documents}

    document_json_map = {}
    for assessment in assessments:
      document_json_map[assessment.id] = [
          documents_map[document_id].log_json_base()
          for document_id in assessment_document_map[assessment.id]
      ]
    return document_json_map

  @staticmethod
  def _get_snapshots_json(assessment, assessment_snapshot_map, snapshots_map):
    snapshots_json = []
    for snapshot_id in assessment_snapshot_map[assessment.id]:
      snapshot = snapshots_map[snapshot_id]
      snapshot_json = snapshot.log_json_base()
      # We avoid using snapshot.revision.log_json_base() to reduce the amount
      # of data being sent to the client.
      snapshot_json["revision"] = {
          "content": {"title": snapshot.revision.content["title"]}
      }
      snapshots_json.append(snapshot_json)
    return snapshots_json

  def _get_snapshots(self, obj, assessments):
    assessment_type = obj.__class__.__name__
    if assessment_type == "Assessment":
      assessment_type = obj.assessment_type
    assessment_ids = [asmt.id for asmt in assessments]

    snapshot_base_query = models.Snapshot.eager_inclusions(
        models.Snapshot.query.options(
            orm.Load(models.Snapshot).undefer_group("Snapshot_complete")
        ),
        ["revision"]
    )

    source_query = db.session.query(
        models.Relationship.destination_id.label("assessment_id"),
        models.Relationship.source_id.label("snapshot_id")
    ).join(
        models.Snapshot,
        and_(
            models.Relationship.source_type == models.Snapshot.__name__,
            models.Relationship.source_id == models.Snapshot.id
        )
    ).filter(
        models.Relationship.destination_id.in_(assessment_ids),
        models.Relationship.destination_type == models.Assessment.__name__,
        models.Snapshot.child_type == assessment_type
    )

    destination_query = db.session.query(
        models.Relationship.source_id.label("assessment_id"),
        models.Relationship.destination_id.label("snapshot_id")
    ).join(
        models.Snapshot,
        and_(
            models.Relationship.destination_type == models.Snapshot.__name__,
            models.Relationship.destination_id == models.Snapshot.id
        )
    ).filter(
        models.Relationship.source_id.in_(assessment_ids),
        models.Relationship.source_type == models.Assessment.__name__,
        models.Snapshot.child_type == assessment_type
    )

    assessment_snapshot_map = defaultdict(set)
    all_snapshot_ids = set()
    for assessment_id, snapshot_id in source_query.union(destination_query):
      assessment_snapshot_map[assessment_id].add(snapshot_id)
      all_snapshot_ids.add(snapshot_id)

    snapshots = snapshot_base_query.filter(
        models.Snapshot.id.in_(all_snapshot_ids)
    ).all()

    snapshots_map = {snapshot.id: snapshot for snapshot in snapshots}

    snapshot_json_map = {}
    for assessment in assessments:
      snapshot_json_map[assessment.id] = self._get_snapshots_json(
          assessment,
          assessment_snapshot_map,
          snapshots_map,
      )

    return snapshot_json_map

  def dispatch_request(self, *args, **kwargs):  # noqa
    """Dispatch request for related_assessments."""
    with benchmark("dispatch related_assessments request"):
      try:

        object_type = request.args.get("object_type")
        object_id = int(request.args.get("object_id"))
        order_by = request.args.get("order_by", "")
        limit_string = request.args.get("limit", "")
        limit = [int(i) for i in limit_string.split(",") if i]

        if request.method != 'GET':
          raise BadRequest()

        model = models.inflector.get_model(object_type)
        obj = model.query.get(object_id)

        with benchmark("get related assessments"):
          assessments, total = self._get_assessments(
              model, object_type, object_id, order_by, limit)

        with benchmark("get documents of related assessments"):
          document_json_map = self._get_documents(assessments)
        with benchmark("get snapshots of related assessments"):
          snapshot_json_map = self._get_snapshots(obj, assessments)

        with benchmark("generate related_assessment json"):
          assessments_json = []
          for assessment in assessments:
            single_json = assessment.log_json_base()
            single_json["audit"] = assessment.audit.log_json_base()
            single_json["custom_attribute_values"] = [
                cav.log_json_base()
                for cav in assessment.custom_attribute_values
            ]
            single_json["custom_attribute_definitions"] = [
                cad.log_json_base()
                for cad in assessment.custom_attribute_definitions
            ]
            single_json["snapshots"] = snapshot_json_map[assessment.id]
            single_json["documents"] = document_json_map[assessment.id]
            assessments_json.append(single_json)

          return self.json_success_response(assessments_json, )

      except (ValueError, TypeError, AttributeError, BadQueryException):
        # Type Error and Value Error are for invalid integer values,
        # Attribute error is for invalid models passed, which return None type
        # that does not have query attribute.
        # Bad query exception is for invalid parameters for limit such as
        # negative numbers.
        raise BadRequest()
