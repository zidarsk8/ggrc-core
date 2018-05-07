# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Migrate documents to evidence

Create Date: 2018-03-28 13:10:43.600584
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from sqlalchemy.sql import text
from alembic import op
from ggrc.migrations import utils
from ggrc.migrations.utils import migrator

# revision identifiers, used by Alembic.

revision = '7b9aae5d448a'
down_revision = '207955a2d3c1'


def get_docs_to_migrate_count(connection):
  """Returns count of documents to migrate"""
  sql = """
  SELECT COUNT(*) FROM (
    SELECT
      d.id
    FROM
      documents as d
    JOIN relationships as r
      ON r.destination_id = d.id
    WHERE
      r.destination_type = 'Document' AND
      d.kind IN ('FILE', 'URL') AND
      r.source_type IN ('Audit', 'Assessment')
    UNION ALL
    SELECT
      d.id
    FROM
      documents as d
    JOIN relationships as r
      ON r.source_id = d.id
    WHERE
      r.source_type = 'Document' AND
      d.kind IN ('FILE', 'URL') AND
      r.destination_type IN ('Audit', 'Assessment')
      ) as ut
  """
  return connection.execute(text(sql)).scalar()


def get_docs_to_migrate(connection):
  """ Returns list of Audit-scope documents (mapped to Audit and Assessment)"""
  sql = """
  SELECT
    d.id as doc_id, d.modified_by_id, d.title, d.link,
    d.description, d.context_id, d.source_gdrive_id,
    d.gdrive_id, d.kind, r.id as rel_id,
    r.source_id as counterparty_id,
    r.source_type as counterparty_type
  FROM
    documents as d
  JOIN relationships as r
    ON r.destination_id = d.id
  WHERE
    r.destination_type = 'Document' AND
    d.kind IN ('FILE', 'URL') AND
    r.source_type IN ('Audit', 'Assessment')
  UNION ALL
  SELECT
    d.id as doc_id, d.modified_by_id, d.title, d.link,
    d.description, d.context_id, d.source_gdrive_id, d.gdrive_id,
    d.kind, r.id as rel_id,
    r.destination_id as counterparty_id,
    r.destination_type as counterparty_type
  FROM
    documents as d
  JOIN relationships as r
    ON r.source_id = d.id
  WHERE
    r.source_type = 'Document' AND
    d.kind IN ('FILE', 'URL') AND
    r.destination_type IN ('Audit', 'Assessment')
  """
  return connection.execute(text(sql))


def create_evidence(connection, doc, migration_user_id):
  """Create evidence record"""
  sql = """
      INSERT INTO evidence (
        modified_by_id,
        created_at,
        updated_at,
        title,
        link,
        description,
        context_id,
        kind,
        source_gdrive_id,
        gdrive_id)
      VALUES (:modified_by_id, NOW(), NOW(), :title, :link,
              :description, :context_id, :kind, :source_gdrive_id, :gdrive_id)
      """
  connection.execute(text(sql),
                     modified_by_id=migration_user_id,
                     title=doc.title,
                     link=doc.link,
                     description=doc.description,
                     context_id=doc.context_id,
                     kind=doc.kind,
                     source_gdrive_id=doc.source_gdrive_id,
                     gdrive_id=doc.gdrive_id)

  evidence_id = utils.last_insert_id(connection)
  slug = 'EVIDENCE-{}'.format(evidence_id)
  set_evidence_slug(connection, evidence_id, slug)
  utils.add_to_objects_without_revisions(connection, evidence_id, "Evidence")
  return evidence_id


def set_evidence_slug(connection, evidence_id, slug):
  """Update evidence slug"""
  slug_sql = """
      UPDATE evidence SET slug=:slug WHERE id=:id
  """
  connection.execute(text(slug_sql),
                     slug=slug,
                     id=evidence_id)


def get_evidence_admin_acls(connection, evidence_id):
  """Return evidence admin acl"""
  sql = """
  SELECT
    acl.ac_role_id,
    acl.context_id,
    acl.created_at,
    acl.updated_at,
    acl.object_id,
    acl.person_id,
    acl.modified_by_id,
    acl.id
  FROM access_control_list acl
    WHERE acl.object_type='Evidence' AND acl.object_id=:evidence_id
  """
  return connection.execute(text(sql), evidence_id=evidence_id)


def create_relationship(connection, source_id, source_type,
                        evid_id, migration_user_id):
  """Create relationship for Evidence"""
  sql = """
      INSERT INTO relationships (
        source_id,
        source_type,
        destination_id,
        destination_type,
        created_at,
        updated_at,
        modified_by_id,
        is_external)
      VALUES (:source_id, :source_type, :evid_id,
              'Evidence', NOW(), NOW(), :modified_by_id, '0');
  """
  connection.execute(text(sql),
                     source_id=source_id,
                     source_type=source_type,
                     evid_id=evid_id,
                     modified_by_id=migration_user_id)
  inserted_id = utils.last_insert_id(connection)
  utils.add_to_objects_without_revisions(connection, inserted_id,
                                         "Relationship")
  return inserted_id


def copy_acl(connection, acl, evidence_id, evid_admin_role_id,
             migration_user_id):
  """Create copy of ACL object"""
  sql = """
      INSERT INTO access_control_list (
        person_id,
        ac_role_id,
        object_id,
        object_type,
        modified_by_id,
        context_id,
        parent_id,
        created_at,
        updated_at)
      VALUES (:person_id, :ac_role_id, :evidence_id, :object_type,
              :modified_by_id, :context_id, :parent_id, NOW(), NOW())
  """
  connection.execute(text(sql),
                     person_id=acl.person_id,
                     ac_role_id=evid_admin_role_id,
                     evidence_id=evidence_id,
                     object_type='Evidence',
                     modified_by_id=migration_user_id,
                     context_id=acl.context_id,
                     parent_id=acl.parent_id)
  acl_id = utils.last_insert_id(connection)
  utils.add_to_objects_without_revisions(connection, acl_id,
                                         "AccessControlList")


# pylint: disable=too-many-arguments
def copy_admin_acls(connection, doc_id, evidence_id, doc_admin_role_id,
                    evid_admin_role_id, migration_user_id):
  """Copy admin acl from document to evidence"""
  results = connection.execute(text("""
      SELECT
        acl.id,
        acl.person_id,
        acl.ac_role_id,
        acl.object_id,
        acl.object_type,
        acl.modified_by_id,
        acl.context_id,
        acl.parent_id
      FROM access_control_list acl
      WHERE acl.object_type = 'Document'
      AND acl.object_id = :doc_id
      AND acl.ac_role_id = :admin_role_id
  """), doc_id=doc_id, admin_role_id=doc_admin_role_id).fetchall()

  for item in results:
    copy_acl(connection, item, evidence_id,
             evid_admin_role_id, migration_user_id)


def get_document_admin_role_id(connection):
  """Returns Document Admin role id"""
  sql = """
    SELECT acr.id  FROM access_control_roles acr WHERE
      acr.object_type='Document' AND name='Admin'
  """
  return connection.execute(text(sql)).fetchone()[0]


def build_acr_mapping(connection):
  """Build mapping for document admin role id to evidence admin role id"""
  sql = """
  SELECT acr1.id as acr_doc_id, acr2.id as acr_evid_id FROM
    access_control_roles acr1
    JOIN access_control_roles acr2 ON acr1.name=acr2.name
    WHERE acr1.object_type='Document'
      AND acr1.name='Admin'
      AND acr2.object_type='Evidence'
      AND acr2.name='Admin'
  """
  doc_admin_role_id, evid_admin_role_id = connection.execute(
      text(sql)).fetchone()

  return doc_admin_role_id, evid_admin_role_id


def delete_document_relationship(connection, rel_id):
  """Delete document relationship"""
  connection.execute(text('DELETE from relationships '
                          'where id = :rel_id'),
                     rel_id=rel_id)


def delete_migrated_document(connection, document_id):
  """Delete document"""
  connection.execute(text('DELETE from documents '
                          'where id = :document_id'),
                     document_id=document_id)


def process_doc(connection, doc, migration_user_id,
                doc_admin_role_id, evid_admin_role_id):
  """Process transformation from document to evidence"""

  evidence_id = create_evidence(connection, doc, migration_user_id)
  copy_admin_acls(connection, doc.doc_id, evidence_id, doc_admin_role_id,
                  evid_admin_role_id, migration_user_id)
  create_relationship(connection, doc.counterparty_id,
                      doc.counterparty_type, evidence_id, migration_user_id)
  delete_migrated_document(connection, doc.doc_id)
  delete_document_relationship(connection, doc.rel_id)


def run_migration():
  """Run migration"""
  connection = op.get_bind()
  migration_user_id = migrator.get_migration_user_id(connection)
  count = get_docs_to_migrate_count(connection)
  docs_to_migrate = get_docs_to_migrate(connection)
  doc_admin_role_id, evid_admin_role_id = build_acr_mapping(connection)
  for i, doc in enumerate(docs_to_migrate):
    print "Processing document {} of {}".format(i, count)
    process_doc(connection, doc, migration_user_id,
                doc_admin_role_id, evid_admin_role_id)


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  run_migration()


def downgrade():
  """This migration contains data migration only. No need to downgrade"""
