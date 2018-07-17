# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add Foreign key Snapshot - Audit

Delete snapshots that doesn't have correct parent_id or parent_type
Create foreign key for linking snapshots.parent_id and audits.id
Create Date: 2018-07-06 14:08:27.860421
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op

# revision identifiers, used by Alembic.
revision = '0e40a37a05f4'
down_revision = '054d15be7a29'


COLLECT_BAD_SNAPSHOT_IDS = """
    INSERT INTO `tmp_bad_snapshots`
    SELECT `s`.`id` AS `id`
    FROM `snapshots` AS `s`
    LEFT JOIN `audits` AS `a`
    ON `s`.`parent_id` = `a`.`id`
    WHERE `a`.`id` IS null OR `s`.`parent_type` != "Audit"
"""


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  connection = op.get_bind()
  op.execute("SET AUTOCOMMIT = 1")
  connection.execute(
      "CREATE TEMPORARY TABLE `tmp_bad_snapshots`(`id` INT(11))"
  )
  if connection.execute(COLLECT_BAD_SNAPSHOT_IDS).rowcount:
    connection.execute(
        """
        DELETE FROM snapshots
        WHERE id IN (SELECT `id` FROM `tmp_bad_snapshots`)
        """
    )
    connection.execute(
        """
        DELETE FROM access_control_list
        WHERE
            object_id IN (SELECT `id` FROM `tmp_bad_snapshots`)
            AND
            object_type = "Snapshot"
        """
    )
    connection.execute(
        """
        DELETE FROM relationships
        WHERE
            source_id IN (SELECT `id` FROM `tmp_bad_snapshots`)
            AND
            source_type = "Snapshot";
        """
    )
    # Because temporary table can't be used twice in one query, deletion
    # of relationships made in 2 queries.
    connection.execute(
        """
        DELETE FROM relationships
        WHERE
            destination_id IN (SELECT `id` FROM `tmp_bad_snapshots`)
            AND
            destination_type = "Snapshot";
        """
    )
  connection.execute("DROP TABLE IF EXISTS `tmp_bad_snapshots`")
  op.execute("SET AUTOCOMMIT = 0")
  op.create_foreign_key(
      'fk_snapshots_audits',
      'snapshots',
      'audits',
      ['parent_id'],
      ['id'],
      ondelete="CASCADE",
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_constraint('fk_snapshots_audits', 'snapshots', type_='foreignkey')
  op.drop_index('fk_snapshots_audits', table_name='snapshots')
