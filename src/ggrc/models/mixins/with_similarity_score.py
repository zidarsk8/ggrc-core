# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Contains WithSimilarityScore mixin.

This defines a procedure of getting "similar" objects which have similar
relationships.
"""

from sqlalchemy import and_
from sqlalchemy import case
from sqlalchemy import literal
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from sqlalchemy.sql import func

from ggrc import db
from ggrc.models.relationship import Relationship


class WithSimilarityScore(object):
  """Defines a routine to get similar object with mappings to same objects."""

  # pylint: disable=too-few-public-methods

  # example of similarity_options:
  # similarity_options = {
  #     "relevant_types": {"Audit": {"weight": 5}, type: {"weight": w}},
  #     "threshold": 10,
  # }

  @classmethod
  def get_similar_objects_query(cls, id_, types="all", relevant_types=None,
                                threshold=None):
    """Get objects of types similar to cls instance by their mappings.

    Args:
      id_: the id of the object to which the search will be applied;
      types: a list of types of relevant objects (or "all" if you need to find
             objects of any type);
      relevant_types: use this parameter to override parameters from
                      cls.similarity_options["relevant_types"];
      threshold: use this parameter to override
                 cls.similarity_options["threshold"].

    Returns:
      SQLAlchemy query that yields results with columns [(id, type, weight)] -
          the id and type of similar objects with respective weights.
    """
    if not types or (not isinstance(types, list) and types != "all"):
      raise ValueError("Expected types = 'all' or a non-empty list of "
                       "requested types, got {!r} instead.".format(types))
    if not hasattr(cls, "similarity_options"):
      raise AttributeError("Expected 'similarity_options' defined for "
                           "'{c.__name__}' model.".format(c=cls))
    if relevant_types is None:
      relevant_types = cls.similarity_options["relevant_types"]
    if threshold is None:
      threshold = cls.similarity_options["threshold"]

    # naming: self is "object", the object mapped to it is "related",
    # the object mapped to "related" is "similar"

    queries_for_union = []

    # find "similar" objects with Relationship table
    queries_for_union += cls._join_relationships(id_)

    # find "similar" objects when Relationship table is not used
    queries_for_union += cls._emulate_relationships(id_, types, relevant_types)

    joined = queries_for_union.pop().union(*queries_for_union).subquery()

    # define weights for every "related" object type with values from
    # relevant_types dict
    weight_case = case(
        [(joined.c.related_type == type_, parameters["weight"])
         for type_, parameters in relevant_types.items()],
        else_=0)
    weight_sum = func.sum(weight_case).label("weight")

    # return the id and type of "similar" object together with its measure of
    # similarity
    result = db.session.query(
        joined.c.similar_id.label("id"),
        joined.c.similar_type.label("type"),
        weight_sum,
    ).filter(or_(
        # filter out self
        joined.c.similar_id != id_,
        joined.c.similar_type != cls.__name__,
    ))

    # do the filtering by "similar" object types
    if types is not None:
      if not types:
        # types is provided but is empty
        return []
      elif types == "all":
        # any type will pass, no filtering applied
        pass
      else:
        # retain only types from the provided list
        result = result.filter(joined.c.similar_type.in_(types))

    # group by "similar" objects to sum up weights correctly
    result = result.group_by(
        joined.c.similar_type,
        joined.c.similar_id,
    ).having(
        # filter out "similar" objects that have insufficient similarity
        weight_sum >= threshold,
    )

    return result

  @classmethod
  def _join_relationships(cls, id_):
    """Make a self-join of Relationship table to find common mappings.

    Returns a query with results for [(related_type, similar_id, similar_type)]
    where similar_id and similar_type describe a second-tier mapped object and
    related_type is the type of a common mapped object between "object" and
    "similar".
    """
    # get all Relationships for self
    object_to_related = db.session.query(Relationship).filter(
        or_(and_(Relationship.source_type == cls.__name__,
                 Relationship.source_id == id_),
            and_(Relationship.destination_type == cls.__name__,
                 Relationship.destination_id == id_))).subquery()

    # define how to get id and type of "related" objects
    related_id_case = (case([(and_(object_to_related.c.source_id == id_,
                                   object_to_related.c.source_type ==
                                   cls.__name__),
                              object_to_related.c.destination_id)],
                            else_=object_to_related.c.source_id)
                       .label("related_id"))
    related_type_case = (case([(and_(object_to_related.c.source_id == id_,
                                     object_to_related.c.source_type ==
                                     cls.__name__),
                                object_to_related.c.destination_type)],
                              else_=object_to_related.c.source_type)
                         .label("related_type"))

    related_to_similar = aliased(Relationship, name="related_to_similar")

    # self-join Relationships to get "similar" id and type; save "related" type
    # to get the weight of this relationship later
    return [
        db.session.query(
            related_type_case,
            related_to_similar.destination_id.label("similar_id"),
            related_to_similar.destination_type.label("similar_type"),
        ).join(
            related_to_similar,
            and_(related_id_case == related_to_similar.source_id,
                 related_type_case == related_to_similar.source_type),
        ),
        db.session.query(
            related_type_case,
            related_to_similar.source_id.label("similar_id"),
            related_to_similar.source_type.label("similar_type"),
        ).join(
            related_to_similar,
            and_(related_id_case == related_to_similar.destination_id,
                 related_type_case == related_to_similar.destination_type),
        ),
    ]

  @classmethod
  def _emulate_relationships(cls, id_, types, relevant_types):
    """Get a list of queries for second-tier objects mapped via foreign key.

    This is used primarily to determine Requests mapped to Audits (Request
    model has a foreign key to Audit model and is not mapped with a
    Relationship object).

    Each query returns results compliant with the results of
    _join_relationships as they get UNIONed.
    """

    # Note: this is a hack that can go away only when Request-Audit mapping
    # will be implemented in Relationships table

    from ggrc.models import Audit, Request

    result = []
    if Audit.__name__ in relevant_types:
      # Note: this code assumes that `types` is a single-element list
      if cls is Request and Request.__name__ in types:
        similar_requests = aliased(cls, name="similar_requests")
        result.append(db.session.query(
            literal(Audit.__name__).label("related_type"),
            similar_requests.id.label("similar_id"),
            literal(Request.__name__).label("similar_type"),
        ).select_from(
            similar_requests,
        ).join(
            cls,
            similar_requests.audit_id == cls.audit_id,
        ).filter(
            and_(cls.id == id_,
                 cls.id != similar_requests.id),
        ))
      elif cls is Request and Request.__name__ not in types:
        audit_to_similar = aliased(Relationship, name="audit_to_similar")
        result.append(db.session.query(
            literal(Audit.__name__).label("related_type"),
            audit_to_similar.source_id.label("similar_id"),
            audit_to_similar.source_type.label("similar_type"),
        ).select_from(
            audit_to_similar,
        ).join(
            cls,
            and_(audit_to_similar.destination_id == cls.audit_id,
                 audit_to_similar.destination_type == Audit.__name__),
        ))
        result.append(db.session.query(
            literal(Audit.__name__).label("related_type"),
            audit_to_similar.destination_id.label("similar_id"),
            audit_to_similar.destination_type.label("similar_type"),
        ).select_from(
            audit_to_similar,
        ).join(
            cls,
            and_(audit_to_similar.source_id == cls.audit_id,
                 audit_to_similar.source_type == Audit.__name__),
        ))
      elif cls is not Request and Request.__name__ in types:
        self_to_audit = aliased(Relationship, name="self_to_audit")
        request = aliased(Request)

        result.append(db.session.query(
            literal(Audit.__name__).label("related_type"),
            request.id.label("similar_id"),
            literal(Request.__name__).label("similar_type"),
        ).select_from(
            request,
        ).join(
            self_to_audit,
            or_(
                and_(self_to_audit.source_id == id_,
                     self_to_audit.source_type == cls.__name__,
                     self_to_audit.destination_id == request.audit_id,
                     self_to_audit.destination_type == Audit.__name__),
                and_(self_to_audit.destination_id == id_,
                     self_to_audit.destination_type == cls.__name__,
                     self_to_audit.source_id == request.audit_id,
                     self_to_audit.source_type == Audit.__name__),
            ),
        ))

    return result
