# Copyright (C) 2015 Reciprocity, Inc - All Rights Reserved
# Unauthorized use, copying, distribution, displaying, or public performance
# of this file, via any medium, is strictly prohibited. All information
# contained herein is proprietary and confidential and may not be shared
# with any third party without the express written consent of Reciprocity, Inc.
# Created By: rok@reciprocitylabs.com
# Maintained By: rok@reciprocitylabs.com

"""Custom attributes should be unique

Revision ID: 1839dabd2357
Revises: 46a791604e98
Create Date: 2015-12-07 15:33:08.728216

"""

from alembic import op
from sqlalchemy.sql import text

from ggrc import db

# revision identifiers, used by Alembic.
revision = '1839dabd2357'
down_revision = '4e989ef86619'


def upgrade():
  """Custom attributes have to be unique, so we find all of those that aren't,
  i.e. they have the same title and definition type and apply a consecutive
  index. Also deleting an attribute should cascade delete values."""

  sql = """
    select    ca.id, ca.title, ca.definition_type
    from      custom_attribute_definitions ca inner join
              custom_attribute_definitions ca2 on (
                ca.title = ca2.title and
                ca.definition_type = ca2.definition_type and
                ca.id != ca2.id)
    group by  ca.id
    order by  ca.title;
  """

  result = db.engine.execute(sql)
  rows = result.fetchall()
  attributes = [dict(zip(result.keys(), r)) for r in rows]
  previous_value = ""
  index = 0
  conn = op.get_bind()
  for a in attributes:
    sql = "update custom_attribute_definitions \
      set title = :title where id = :id"
    if previous_value != a["title"]:
      previous_value = a["title"]
      index = 0
    index += 1
    new_title = "{} {}".format(a["title"], index)
    conn.execute(text(sql), title=new_title, id=a["id"])

  op.create_unique_constraint(
      "uq_custom_attribute", "custom_attribute_definitions",
      ["title", "definition_type"])

  # make custom attributes cascade delete values
  sql1 = """
      alter table  custom_attribute_values
      drop         foreign key custom_attribute_values_ibfk_1"""
  sql2 = """
      alter table  custom_attribute_values
      add          constraint custom_attribute_values_ibfk_1
                   foreign key (custom_attribute_id)
      references   custom_attribute_definitions (id)
      on delete    cascade"""
  op.execute(sql1)
  op.execute(sql2)


def downgrade():
  op.drop_constraint("uq_custom_attribute", "custom_attribute_definitions",
                     type_="unique")

  sql1 = """
      alter table  custom_attribute_values
      drop         foreign key custom_attribute_values_ibfk_1"""
  sql2 = """
      alter table  custom_attribute_values
      add          constraint custom_attribute_values_ibfk_1
                   foreign key (custom_attribute_id)
      references   custom_attribute_definitions (id)"""
  op.execute(sql1)
  op.execute(sql2)
