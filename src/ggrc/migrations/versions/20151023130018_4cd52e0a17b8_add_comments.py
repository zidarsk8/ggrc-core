# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: urban@reciprocitylabs.com

"""Add Comments

Revision ID: 4cd52e0a17b8
Revises: 3c8f204ba7a9
Create Date: 2015-10-23 13:00:18.555497

"""

# revision identifiers, used by Alembic.
revision = '4cd52e0a17b8'
down_revision = '27684e5f313a'

from alembic import op
import sqlalchemy as sa


from ggrc import db
from ggrc.models import Comment
from ggrc.models import DocumentationResponse
from ggrc.models import InterviewResponse
from ggrc.models import Relationship


def upgrade():
  op.create_table(
      'comments',
      sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
      sa.Column('description', sa.Text()),
      sa.Column('created_at', sa.DateTime()),
      sa.Column('modified_by_id', sa.Integer()),
      sa.Column('updated_at', sa.DateTime()),
      sa.Column('context_id', sa.Integer(), sa.ForeignKey('contexts.id'))
  )

  documentation_responses = db.session.query(DocumentationResponse)
  for dr in documentation_responses:
    related = dr.related_sources + dr.related_destinations
    comment = Comment(
      description = dr.description,
      created_at = dr.created_at,
      modified_by = dr.modified_by,
      updated_at = dr.updated_at,
      context = dr.context)

    request_comment_rel = Relationship(
      source=dr.request,
      destination=comment)

    for rel in related:
      if rel.source.type == "DocumentationResponse":
        destination = rel.destination
      elif rel.destination.type == "DocumentationResponse":
        destination = rel.source
      related_objects_to_request = Relationship(
        source=dr.request,
        destination=destination
      )
      db.session.add(related_objects_to_request)
    db.session.add(comment)
    db.session.add(request_comment_rel)
  db.session.commit()

  interview_responses = db.session.query(InterviewResponse)
  for ir  in interview_responses:
    related = ir.related_sources + ir.related_destinations

    desc = ir.description
    if ir.meetings:
      desc += "<br /><br /><b>Meetings</b><hr />"

      for m in ir.meetings:
        desc += "<a href=\"{url}\">Meeting</a> requested on {date}<br />".\
          format(**{
              "url": m.title,
              "date": m.created_at.strftime("%m/%d/%Y at %H:%M"),
            })

    if ir.people:
      desc += "<br /><br /><b>Attendees</b><hr />"
      for p in ir.people:
        desc += "- {} ({})<br />".format(p.name, p.email)

    comment = Comment(
      description = desc,
      created_at = ir.created_at,
      modified_by = ir.modified_by,
      updated_at = ir.updated_at,
      context = ir.context)

    request_comment_rel = Relationship(
      source=ir.request,
      destination=comment)

    for rel in related:
      if rel.source.type == "InterviewResponse":
        destination = rel.destination
      elif rel.destination.type == "InterviewResponse":
        destination = rel.source
      related_objects_to_request = Relationship(
        source=ir.request,
        destination=destination
      )
      db.session.add(related_objects_to_request)
    db.session.add(comment)
    db.session.add(request_comment_rel)
  db.session.commit()


def downgrade():
  op.drop_table('comments')
