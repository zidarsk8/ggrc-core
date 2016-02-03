# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


"""connect requests to audit_objects

Revision ID: d47d1285cf5
Revises: 4da382b50349
Create Date: 2014-06-16 18:00:36.877630

"""

# revision identifiers, used by Alembic.
revision = 'd47d1285cf5'
down_revision = '4da382b50349'

import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy.sql.expression import literal, and_, select
from  sqlalchemy.engine.reflection import Inspector

from alembic import op


def upgrade():
  # ALTER TABLE requests ADD COLUMN (audit_object_id INT NULL);
  op.add_column(
    'requests',
    sa.Column(u'audit_object_id', sa.Integer(), nullable=True))
  # ALTER TABLE requests ADD CONSTRAINT FOREIGN KEY (audit_object_id) 
  #   REFERENCES `audit_objects` (`id`) ON DELETE SET NULL;
  op.create_foreign_key(
      u'requests_audit_objects_ibfk',
      u'requests',
      u'audit_objects',
      [u'audit_object_id'],
      [u'id'])

  audit_objects_table = table('audit_objects',
    column('id', sa.Integer),
    column('audit_id', sa.Integer),
    column('auditable_id', sa.Integer),
    column('context_id', sa.Integer),
    column('auditable_type', sa.String),
    column('modified_by_id', sa.Integer),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime)
    )

  requests_table = table('requests',
    column('audit_id', sa.Integer),
    column('objective_id', sa.Integer),
    column('context_id', sa.Integer),
    column('audit_object_id', sa.Integer),
    column('modified_by_id', sa.Integer),
    column('created_at', sa.DateTime),
    column('updated_at', sa.DateTime)
    )

  # INSERT INTO audit_objects (audit_id, auditable_id, context_id, auditable_type) 
  # SELECT DISTINCT r.audit_id, r.objective_id, r.context_id, "Objective" as auditable_type
  # FROM requests r LEFT OUTER JOIN audit_objects ao 
  #   ON r.audit_id = ao.audit_id
  #   AND ao.auditable_id = r.objective_id
  #   AND ao.auditable_type = "Objective"
  # WHERE r.objective_id IS NOT NULL
  # AND ao.auditable_id IS NULL
  # -- NB: This is better understood as "find all request objective IDs
  #    that aren't yet hooked up to the request's audit, and add them to audit_objects"
  #    but subquery is more challenging in SQLAlchemy, so here it is written as an outer
  #    join.  --BM
  r = requests_table.alias('r')
  ao = audit_objects_table.alias('ao')
  op.execute(audit_objects_table.insert()\
    .from_select(
      [ 'audit_id', 'auditable_id', 'context_id', 'auditable_type'
        ],
      select(
        from_obj=r.outerjoin(
          ao, 
          onclause=and_(
            r.c.audit_id == ao.c.audit_id,
            ao.c.auditable_id == r.c.objective_id,
            ao.c.auditable_type == "Objective"
          )),
        columns=[ r.c.audit_id, r.c.objective_id, r.c.context_id, literal('Objective')
                  ],
        distinct=True,
        ).where(
          and_(
            r.c.objective_id != None,
            ao.c.auditable_id == None
        ))
      ))

  # UPDATE requests r, audit_objects ao 
  #   set r.audit_object_id = ao.id 
  #   where  ao.audit_id = r.audit_id 
  #   AND ao.auditable_id = r.objective_id 
  #   AND ao.auditable_type = 'Objective';
  op.execute(requests_table.update()\
    .where(\
      and_(\
        ao.c.audit_id == requests_table.c.audit_id,
        ao.c.auditable_id == requests_table.c.objective_id,
        ao.c.auditable_type == "Objective"
        ))\
    .values(audit_object_id=ao.c.id)\
    )

  # UPDATE audit_objects, requests
  # SET audit_objects.created_at=requests.updated_at,
  #     audit_objects.updated_at=requests.updated_at,
  #     audit_objects.modified_by_id=requests.modified_by_id
  # WHERE requests.audit_object_id=audit_objects.id
  # -- NB: The syntax below is weird and doesn't really line
  # --  up with the SQL above, but it's the SQLAlchemy-blessed
  # --  way of stating it (see the docs). --BM
  op.execute(
    audit_objects_table.update()
      .values(created_at=select([requests_table.c.updated_at])
                         .where(requests_table.c.audit_object_id == audit_objects_table.c.id)
                         .limit(1).as_scalar(),
              updated_at=select([requests_table.c.updated_at])
                         .where(requests_table.c.audit_object_id == audit_objects_table.c.id)
                         .limit(1).as_scalar(),
              modified_by_id=select([requests_table.c.modified_by_id])
                             .where(requests_table.c.audit_object_id == audit_objects_table.c.id)
                             .limit(1).as_scalar()
      ))

  # SELECT @fk:=constraint_name FROM information_schema.referential_constraints 
  #   WHERE constraint_schema = DATABASE() 
  #   AND table_name = 'requests' 
  #   AND referenced_table_name = 'objectives';
  # SET @drop_ro_fk_sql:=CONCAT('ALTER TABLE requests DROP FOREIGN KEY ', @fk);
  # PREPARE drop_ro_fk FROM drop_ro_fk_sql;
  # EXECUTE drop_ro_fk;
  # DEALLOCATE PREPARE drop_ro_fk;
  constraints_table = table('information_schema.referential_constraints',
    column('constraint_name', sa.String),
    column('constraint_schema', sa.String),
    column('table_name', sa.String),
    column('referenced_table_name', sa.String),
    )

  # fks *should* only contain requests_ibfk_4, but I don't entirely trust it
  #  because I can't see all deployed DBs --BM
  fks = [x['name'] 
          for x in Inspector(op.get_bind()).get_foreign_keys('requests') 
          if x['referred_table'] == 'objectives'
          ];

  for fk in fks:
    op.drop_constraint(fk, u'requests', 'foreignkey')

  # ALTER TABLE requests DROP COLUMN `objective_id`;
  op.drop_column('requests', 'objective_id')



def downgrade():
  # ALTER TABLE requests ADD COLUMN (objective INT NULL);
  op.add_column(
    'requests',
    sa.Column(u'objective_id', sa.Integer(), nullable=True))
  # ALTER TABLE requests ADD CONSTRAINT FOREIGN KEY 
  #  (objective_id) REFERENCES objectives (id) ON DELETE SET NULL;
  op.create_foreign_key(
      u'requests_ibfk_4',
      u'requests',
      u'objectives',
      [u'objective_id'],
      [u'id'])

  audit_objects_table = table('audit_objects',
    column('id', sa.Integer),
    column('auditable_id', sa.Integer),
    column('auditable_type', sa.String)
    )

  requests_table = table('requests',
    column('objective_id', sa.Integer),
    column('audit_object_id', sa.Integer),
    )

  # UPDATE requests r, audit_objects ao 
  #   SET objective_id = ao.auditable_id 
  #   WHERE ao.id = r.audit_object_id;
  op.execute(requests_table.update()\
    .values(
      objective_id=select([audit_objects_table.c.auditable_id])
        .where(
          and_(
            requests_table.c.audit_object_id == audit_objects_table.c.id,
            audit_objects_table.c.auditable_type == 'Objective'
            )
          )
        .correlate(requests_table).as_scalar()
    ))

  # ALTER TABLE requests DROP FOREIGN KEY requests_audit_objects_ibfk
  op.drop_constraint(u'requests_audit_objects_ibfk', u'requests', 'foreignkey')

  # ALTER TABLE requests DROP COLUMN `audit_object_id`;
  op.drop_column('requests', 'audit_object_id')
