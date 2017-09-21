# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Assessment API resource optimization."""

from werkzeug.exceptions import Forbidden
from sqlalchemy import orm

from ggrc import db
from ggrc import models
from ggrc.utils import benchmark
from ggrc.rbac import permissions
from ggrc.services import common


class AssessmentResource(common.ExtendedResource):
  """Resource handler for Assessments."""

  # method post is abstract and not used.
  # pylint: disable=abstract-method

  def get(self, *args, **kwargs):
    # This is to extend the get request for additional data.
    # pylint: disable=arguments-differ
    command_map = {
        None: super(AssessmentResource, self).get,
        "related_objects": self.related_objects,
    }
    command = kwargs.pop("command", None)
    if command not in command_map:
      self.not_found_response()
    return command_map[command](*args, **kwargs)

  @staticmethod
  def _get_relationships_data(relationships):
    """Return serialized all relationships needed for assessment page."""
    return [rel.log_json() for rel in relationships]

  @staticmethod
  def _get_relationships(assessment):
    """Get all relationships for the current assessment."""
    relationships = models.Relationship.eager_query().filter(
        models.Relationship.source_type == assessment.type,
        models.Relationship.source_id == assessment.id,
    ).all()
    relationships += models.Relationship.eager_query().filter(
        models.Relationship.destination_type == assessment.type,
        models.Relationship.destination_id == assessment.id,
    ).all()
    return relationships

  @staticmethod
  def _get_audit_data(assessment):
    """Get audit title for the assessment related audit.

    This function is just a bit optimized way of returning
    assessment.audit.title
    """
    title = db.session.query(models.Audit.title).filter_by(
        id=assessment.audit_id).scalar()
    return {"title": title}

  @staticmethod
  def _filter_rels(relationships, type_):
    """Filter assessment related objects by related type.

    Args:
      relationships: list of all assessment relationships
      type_: related object type

    Returns:
      list of ids of all related objects for the given type.
    """
    ids = [rel.source_id for rel in relationships if type_ in rel.source_type]
    ids.extend(rel.destination_id for rel in relationships
               if type_ in rel.destination_type)
    return ids

  def _get_snapshot_data(self, assessment, relationships):
    """Get snapshot data for the current assessment:

    Args:
      relationships: List of all relationships related to the current
        assessment.
    """
    relationship_ids = self._filter_rels(relationships, "Snapshot")
    with benchmark("Get assessment snapshot relationships"):
      snapshots = models.Snapshot.query.options(
          orm.undefer_group("Snapshot_complete"),
          orm.joinedload('revision'),
      ).filter(
          models.Snapshot.id.in_(relationship_ids)
      ).all()
    with benchmark("Set assessment snapshot relationships"):
      data = []
      for snapshot in snapshots:
        data.append({
            "archived": assessment.audit.archived,
            "revision": snapshot.revision.log_json(),
            "related_sources": [],
            "parent": {
                "context_id": assessment.context_id,
                "href": "/api/audits/{}".format(assessment.audit_id),
                "type": "Audit",
                "id": assessment.audit_id,
            },
            "child_type": snapshot.child_type,
            "child_id": snapshot.child_id,
            "related_destinations": [],
            "id": snapshot.id,
            "revisions": [],
            "revision_id": snapshot.revision_id,
            "type": snapshot.type,
        })
    return data

  def _get_document_data(self, relationships):
    """Get assessment document data.

    Args:
      relationships: list of all relationships for the current assessment.

    Returns:
      data for related urls, reference urls, and attachments.
    """
    relationship_ids = self._filter_rels(relationships, "Document")
    with benchmark("Get assessment snapshot relationships"):
      documents = models.Document.eager_query().filter(
          models.Document.id.in_(relationship_ids)
      ).all()
    urls = [doc.log_json() for doc in documents
            if doc.document_type == doc.URL]
    ref_urls = [doc.log_json() for doc in documents
                if doc.document_type == doc.REFERENCE_URL]
    attachments = [doc.log_json() for doc in documents
                   if doc.document_type == doc.ATTACHMENT]
    return urls, ref_urls, attachments

  def _get_comment_data(self, relationships):
    """Get assessment comment data."""
    relationship_ids = self._filter_rels(relationships, "Comment")
    with benchmark("Get assessment comment data"):
      comments = models.Comment.eager_query().filter(
          models.Comment.id.in_(relationship_ids)
      ).all()
    return [comment.log_json() for comment in comments]

  def _get_people_data(self, relationships):
    """Get assessment people data.

    This function returns data for people related to the assessment without
    ACL roles. The data does not include the relationships since those are
    sent in a different block.
    """
    relationship_ids = self._filter_rels(relationships, "Person")
    with benchmark("Get assessment snapshot relationships"):
      people = models.Person.query.options(
          orm.undefer_group("Person_complete"),
          orm.joinedload('language'),
          orm.subqueryload('object_people'),
          orm.subqueryload('_custom_attribute_values').undefer_group(
              'CustomAttributeValue_complete'
          )
      ).filter(
          models.Person.id.in_(relationship_ids)
      ).all()
    return [person.log_json() for person in people]

  def _get_related_data(self, assessment):
    """Get assessment related data.

    This function should return all data needed for displaying a full
    assessment.
    """
    relationships = self._get_relationships(assessment)
    urls, ref_urls, attachments = self._get_document_data(relationships)
    urls_key = "Document:{}".format(models.Document.URL)
    attachments_key = "Document:{}".format(models.Document.ATTACHMENT)
    ref_urls_key = "Document:{}".format(models.Document.REFERENCE_URL)
    data = {
        "Relationship": self._get_relationships_data(relationships),
        "Audit": self._get_audit_data(assessment),
        "Snapshot": self._get_snapshot_data(assessment, relationships),
        "Comment": self._get_comment_data(relationships),
        "Person": self._get_people_data(relationships),
        urls_key: urls,
        ref_urls_key: ref_urls,
        attachments_key: attachments,
    }
    return data

  def related_objects(self, id):
    """Get data for assessment related_objects page."""
    # id name is used as a kw argument and can't be changed here
    # pylint: disable=invalid-name,redefined-builtin
    with benchmark("check assessment permissions"):
      assessment = models.Assessment.query.options(
          orm.undefer_group("Assessment_complete")
      ).get(id)
      if not permissions.is_allowed_read_for(assessment):
        raise Forbidden()
    with benchmark("Get assessment related_objects data"):
      data = self._get_related_data(assessment)
    with benchmark("Make response"):
      return self.json_success_response(data, )
