
"""Make Request First-class object

Revision ID: 27684e5f313a
Revises: 3c8f204ba7a9
Create Date: 2015-10-16 17:48:06.875436

"""

# revision identifiers, used by Alembic.
revision = '27684e5f313a'
down_revision = '4cd52e0a17b8'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

def upgrade():
    sql = "BEGIN;"
    # 1. Move Audit Objects to Relationship table
    #   source_type = audit_objects.auditable_type
    #   source_id = audit_objects.auditable_id
    #   destination_type = "Request"
    #   destination_id = request.id
    sql += """
    INSERT INTO relationships (
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
    """
    # 2. Create relations to Audits in Relationship table
    #   source_type = Audit
    #   source_id   = audit.id
    #   destionation_type = Request
    #   destination_id = request.id
    sql += """
    INSERT INTO relationships (
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
      AO.audit_id,
      "Audit",
      R.id,
      "Request",
      AO.context_id
      FROM requests AS R, audit_objects AS AO WHERE AO.id = R.audit_object_id;
    """

    # 3. Change status values
    sql += """
    ALTER TABLE requests CHANGE status status ENUM('Draft','Requested','Responded','Amended Request','Updated Response','Accepted','Unstarted','In Progress','Finished','Verified') NOT NULL;

    UPDATE requests SET status='Unstarted' WHERE status='Draft';
    UPDATE requests SET status='In Progress' WHERE status='Requested';
    UPDATE requests SET status='Finished' WHERE status='Responded';
    UPDATE requests SET status='In Progress' WHERE status='Amended Request';
    UPDATE requests SET status='Finished' WHERE status='Updated Response';
    UPDATE requests SET status='Verified' WHERE status='Accepted';

    ALTER TABLE requests CHANGE status status ENUM('Unstarted','In Progress','Finished','Verified') NOT NULL;
    """

    sql += "COMMIT;"
    op.execute(sql)

    # Remove unneeded attributes
    # sql = "BEGIN;"
    # # 3. Drop FK audit_objects_id from Request
    # sql += """
    # ALTER TABLE requests DROP FOREIGN KEY requests_audit_objects_ibfk;
    # DROP INDEX requests_audit_objects_ibfk ON requests;
    # ALTER TABLE requests DROP COLUMN audit_object_id;
    # """
    # # 4. Drop audit_id from Request
    # sql += """
    # ALTER TABLE requests DROP FOREIGN KEY requests_ibfk_2;
    # ALTER TABLE requests DROP COLUMN audit_id;
    # """
    # sql += "COMMIT;"
    # op.execute(sql)


    # TODO: drop requests table from audits

    # TODO: 5. Link all objects that are mapped to Audit to requests

    # TODO: Drop relationship audit_objects from Audits????


def downgrade():
    pass
