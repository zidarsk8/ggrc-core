# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Remove '*' from slugs

Create Date: 2018-07-10 16:01:31.021762
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '0e385718442a'
down_revision = '0e40a37a05f4'


TABLES_WITH_SLUG = {
    'access_groups', 'assessment_templates', 'assessments', 'audits',
    'clauses', 'controls', 'cycle_task_group_object_tasks',
    'cycle_task_groups', 'cycles', 'data_assets', 'directives', 'documents',
    'evidence', 'facilities', 'issues', 'markets', 'metrics', 'objectives',
    'org_groups', 'products', 'programs', 'projects', 'risk_assessments',
    'risks', 'sections', 'systems', 'task_group_tasks', 'task_groups',
    'threats', 'vendors', 'workflows',
}


CREATE_TMP_TABLES = """
CREATE TEMPORARY TABLE `tmp_change_slugs`(
    `tbl` VARCHAR(250),
    `tbl_id` INT(11),
    `tmp_slug` VARCHAR(250),
    `new_slug` VARCHAR(250),

    KEY (`tbl`),
    KEY (`tbl_id`),
    KEY (`new_slug`),
    KEY (`new_slug`, `tbl`)
);
CREATE TEMPORARY TABLE `tmp_cache`(
    `tbl` VARCHAR(250),
    `slug` VARCHAR(250),

    KEY (`tbl`),
    KEY (`slug`)
);
CREATE TEMPORARY TABLE `tmp_same_new_slugs`(
    `tbl` VARCHAR(250),
    `slug` VARCHAR(250),

    KEY (`tbl`),
    KEY (`slug`)
);
"""


DROP_TMP_TABLE = """
DROP TABLE IF EXISTS `tmp_change_slugs`;
DROP TABLE IF EXISTS `tmp_cache`;
DROP TABLE IF EXISTS `tmp_same_new_slugs`;
"""


# Select slugs matching mask, replace '*' to '-' and
# cut slug to fit '{slug}-{INT(11)}' in VARCHAR(250) in worse case scenario
SELECT_MASK_SLUGS = """
SELECT
    '{tbl}',
    `id`,
    LEFT(REPLACE(`slug`, '*', '-'), 238),
    LEFT(REPLACE(`slug`, '*', '-'), 238)
FROM `{tbl}`
WHERE `slug` LIKE :mask
"""

INSERT_SAME_NEW_SLUGS = """
INSERT INTO `tmp_same_new_slugs`
SELECT `tbl`, `new_slug` AS `slug`
FROM `tmp_change_slugs`
GROUP BY `new_slug`, `tbl`
HAVING count(`new_slug`) > 1;
"""


UPDATE_TMP_SLUGS = """
UPDATE `tmp_change_slugs` as `t1`
JOIN `{_join}` as `t2`
ON
    `t1`.`new_slug` = `t2`.`slug`
    AND `t1`.`tbl` = `t2`.`tbl`
SET `t1`.`new_slug` = CONCAT(`t1`.`tmp_slug`, '-', @i:=@i+1)
"""


SELECT_SLUGS = """
SELECT '{tbl}' AS `tbl`, `slug`
FROM `{tbl}`
"""


UPDATE_SLUG = """
UPDATE `{tbl}` AS `t1`
JOIN `tmp_change_slugs` AS `t2`
ON
    `t1`.`id` = `t2`.`tbl_id`
    AND '{tbl}' = `t2`.`tbl`
SET `t1`.`slug` = `t2`.`new_slug`
"""


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  connection = op.get_bind()
  op.execute("SET AUTOCOMMIT = 1")
  connection.execute(CREATE_TMP_TABLES)
  connection.execute("SET @i = 0")  # Variable for generation unique suffixes

  # Collect set of existing tables in db that have 'slug' column
  tables_in_db = set(tbl[0] for tbl in connection.execute("SHOW TABLES")
                     if tbl[0] in TABLES_WITH_SLUG)
  # Insert slugs matching 'mask' to temporary table
  query = "INSERT INTO `tmp_change_slugs`" + "UNION ALL".join(
      SELECT_MASK_SLUGS.format(tbl=tbl) for tbl in tables_in_db
  )
  if not connection.execute(sa.sql.text(query), mask="%*%").rowcount:
    # Quit if query not found matching slugs
    connection.execute(DROP_TMP_TABLE)
    op.execute("SET AUTOCOMMIT = 0")
    return

  # Fix slugs in tmp table in case of same new_slugs
  # example: 'C*-1', 'C-*1'
  connection.execute(INSERT_SAME_NEW_SLUGS)
  connection.execute(UPDATE_TMP_SLUGS.format(_join="tmp_same_new_slugs"))

  # Collect set of tables in tmp_change_slugs
  _tables_query = "SELECT DISTINCT `tbl` FROM `tmp_change_slugs`"
  tables_in_tmp = set(tbl[0] for tbl in connection.execute(_tables_query))
  # Collect slugs in cache table
  query = "INSERT INTO `tmp_cache`" + 'UNION ALL'.join(
      SELECT_SLUGS.format(tbl=tbl) for tbl in tables_in_tmp
  )
  connection.execute(query)
  # Query search for slugs already exists and change suffix
  query = UPDATE_TMP_SLUGS.format(_join="tmp_cache")
  conflicts = connection.execute(query).rowcount
  # Attempt to resolve conflicts, until query affect zero rows
  while conflicts:
    conflicts = connection.execute(query).rowcount

  # Update slugs in DB
  for tbl in tables_in_tmp:
    connection.execute(UPDATE_SLUG.format(tbl=tbl))

  # Drop temporary tables
  connection.execute(DROP_TMP_TABLE)
  op.execute("SET AUTOCOMMIT = 0")


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  pass
