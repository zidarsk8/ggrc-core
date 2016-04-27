# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: urban@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

"""Make Request First-class object

Revision ID: 27684e5f313a
Revises: 3c8f204ba7a9
Create Date: 2015-10-16 17:48:06.875436

"""

# revision identifiers, used by Alembic.
from alembic import op
import bleach
import datetime
from HTMLParser import HTMLParser
import sqlalchemy.exc as sqlaexceptions
import sqlalchemy.types as types
from sqlalchemy.sql import column
from sqlalchemy.sql import table


revision = '27684e5f313a'
down_revision = '1bad7fe16295'


relationships_table = table(
    'relationships',
    column('id'),
    column('source_id'),
    column('source_type'),
    column('destination_id'),
    column('destination_type'),
    column('context_id'),
    column('modified_by_id'),
    column('updated_at'),
    column('created_at'),
)


comments_table = table(
    'comments',
    column('id'),
    column('description'),
    column('created_at'),
    column('modified_by_id'),
    column('updated_at'),
    column('context_id')
)


def cleaner(value, bleach_tags=[], bleach_attrs={}):
  if value is None:
    return value

  parser = HTMLParser()
  lastvalue = value
  value = parser.unescape(value)
  while value != lastvalue:
    lastvalue = value
    value = parser.unescape(value)

  ret = parser.unescape(
      bleach.clean(value, bleach_tags, bleach_attrs, strip=True)
  )
  return ret


def _build_comment(iid,
                   description,
                   created_at,
                   modified_by,
                   updated_at,
                   context,
                   request_id):
  context_id = context.id if context else None
  return {
      "id": iid,
      "description": description,
      "created_at": created_at,
      "modified_by_id": modified_by.id,
      "updated_at": updated_at,
      "context_id": context_id,
      "request_id": request_id,
  }


def _build_request_comment_relationship(req_id,
                                        comm_id,
                                        context_id,
                                        modified_by_id):
  return {
      "source_type": "Request",
      "source_id": req_id,
      "destination_type": "Comment",
      "destination_id": comm_id,
      "context_id": context_id,
      "modified_by_id": modified_by_id,
      "updated_at": datetime.datetime.now(),
      "created_at": datetime.datetime.now()
  }


def _build_request_object_relationship(req, dest):
  relationship = {
      "source_type": "Request",
      "source_id": req.id,
      "destination_type": dest.type,
      "destination_id": dest.id,
      "context_id": req.context.id if req.context else None,
      "updated_at": datetime.datetime.now(),
      "created_at": datetime.datetime.now()
  }
  identifier = (
      'Request',
      relationship['source_id'],
      relationship['destination_type'],
      relationship['destination_id'],
  )
  return (identifier, relationship)


def upgrade():

  # 1. Move Audit Objects to Relationship table
  #   source_type = audit_objects.auditable_type
  #   source_id = audit_objects.auditable_id
  #   destination_type = "Request"
  #   destination_id = request.id
  op.execute("""
    INSERT IGNORE INTO relationships (
      modified_by_id,
      created_at,
      updated_at,
      source_id,
      source_type,
      destination_id,
      destination_type,
      context_id) SELECT
        AO.modified_by_id,
        NOW(),
        NOW(),
        AO.auditable_id,
        AO.auditable_type,
        R.id,
        "Request",
        AO.context_id
      FROM requests AS R, audit_objects AS AO WHERE AO.id = R.audit_object_id;
    """)

  # 2. Change status values
  op.execute(
      """
      ALTER TABLE requests
      CHANGE status status
      ENUM("Draft","Requested","Responded","Amended Request",
      "Updated Response","Accepted","Unstarted","In Progress","Finished",
      "Verified") NOT NULL;"""
  )
  op.execute(
      """
      UPDATE requests SET status="Unstarted"
      WHERE status="Draft";"""
  )
  op.execute(
      """
      UPDATE requests SET status="In Progress"
      WHERE status="Requested";"""
  )
  op.execute(
      """
      UPDATE requests SET status="Finished"
      WHERE status="Responded";"""
  )
  op.execute(
      """
      UPDATE requests SET status="In Progress"
      WHERE status="Amended Request";"""
  )
  op.execute(
      """
      UPDATE requests SET status="Finished"
      WHERE status="Updated Response";"""
  )
  op.execute(
      """
      UPDATE requests SET status="Verified"
      WHERE status="Accepted";"""
  )
  op.execute(
      """
      ALTER TABLE requests CHANGE status status
      ENUM("Unstarted","In Progress","Finished","Verified") NOT NULL;"""
  )

  # Drop foreign key relationship on assignee_id
  try:
    op.drop_constraint("requests_ibfk_1", "requests", type_="foreignkey")
  except sqlaexceptions.OperationalError as oe:
    # Ignores error in case constraint no longer exists
    error_code, _ = oe.orig.args  # error_code, message
    if error_code != 1025:
      raise oe

  # Drop index on assignee_id
  try:
    op.drop_index("assignee_id", "requests")
  except sqlaexceptions.OperationalError as oe:
    # Ignores error in case index no longer exists
    error_code, _ = oe.orig.args  # error_code, message
    if error_code != 1091:
      raise oe

  # Make assignee_id nullable
  op.alter_column("requests", "assignee_id",
                  existing_nullable=False, nullable=True, type_=types.Integer)


def downgrade():
  pass
