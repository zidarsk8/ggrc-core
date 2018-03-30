# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""SQLAlchemy hooks for Workflow model."""

import flask
import sqlalchemy as sa

from ggrc import db
from ggrc import login
from ggrc import utils
from ggrc.models import all_models
from ggrc.access_control import role


RELATED_MODELS = (
    all_models.TaskGroup,
    all_models.TaskGroupTask,
    all_models.TaskGroupObject,
    all_models.Cycle,
    all_models.CycleTaskGroup,
    all_models.CycleTaskGroupObjectTask,
    all_models.CycleTaskEntry,
)

WF_PROPAGATED_ROLES = {
    "Admin",
    "Workflow Member",
}


def handle_acl_changes():
  """ACL creation hook handler.

  The global variables for this function are set in the after_flush hook, so
  this function must be called after that hook in order for propagation to
  work.
  """

  if not (hasattr(flask.g, "new_wf_acls") and
          hasattr(flask.g, "deleted_wf_objects")):
    return

  _propagete_new_wf_acls(flask.g.new_wf_acls)
  remove_related_acl(flask.g.deleted_wf_objects)

  del flask.g.new_wf_acls,
  del flask.g.deleted_wf_objects,


def get_wf_propagated_role_ids():
  """Getting propagated role ids."""
  wf_roles = role.get_custom_roles_for(all_models.Workflow.__name__)
  return {
      id_ for id_, name in wf_roles.items()
      if name in WF_PROPAGATED_ROLES
  }


def get_new_wf_acls(session):
  """Add propagated roles to workflow related objects."""
  propagated_role_ids = None
  new_wf_acls = set()
  for obj in session.new:
    acls = []
    if (isinstance(obj, all_models.AccessControlList) and
            obj.object_type == all_models.Workflow.__name__):
      acls.append(obj)
    elif isinstance(obj, RELATED_MODELS):
      # not optimized operation. Adding a new task will result in full
      # propagation on the entire workflow.
      acls.extend(obj.workflow.access_control_list)
    if propagated_role_ids is None:
      propagated_role_ids = get_wf_propagated_role_ids()
    for acl in acls:
      if acl.ac_role_id in propagated_role_ids:
        new_wf_acls.add(acl.id)
  return new_wf_acls


def get_deleted_wf_objects(session):
  """Remove propagated roles to workflow related objects."""
  related_to_del = set()
  for obj in session.deleted:
    if isinstance(obj, RELATED_MODELS):
      related_to_del.add((obj.type, obj.id))
  return related_to_del


def remove_related_acl(related_to_del):
  """Remove related ACL records on related object delete.

  Args:
      related_to_del: mapping related object type to set of ids to delete
          {
            related_object_type_name1: set(related_id1, ...),
            related_object_type_name2: set(related_id1, ...)
            ...
          }
  """
  if not related_to_del:
    return

  db.session.query(all_models.AccessControlList).filter(
      sa.tuple_(
          all_models.AccessControlList.object_type,
          all_models.AccessControlList.object_id,
      ).in_(related_to_del)
  ).delete(synchronize_session='fetch')


def _get_child_ids(parent_ids, child_class):
  """Get all acl ids for acl entries with the given parent ids

  Args:
    parent_ids: list of parent acl entries or query with parent ids.

  Returns:
    list of ACL ids for all children from the given parents.
  """
  acl_table = all_models.AccessControlList.__table__

  return sa.select([acl_table.c.id]).where(
      acl_table.c.parent_id.in_(parent_ids)
  ).where(
      acl_table.c.object_type == child_class.__name__
  )


def _insert_select_acls(select_statement):
  """Insert acl records from the select statement

  Args:
    select_statement: sql statement that contains the following columns
      person_id,
      ac_role_id,
      object_id,
      object_type,
      created_at,
      modified_by_id,
      updated_at,
      parent_id,
  """

  acl_table = all_models.AccessControlList.__table__

  inserter = acl_table.insert().prefix_with("IGNORE")

  db.session.execute(
      inserter.from_select(
          [
              acl_table.c.person_id,
              acl_table.c.ac_role_id,
              acl_table.c.object_id,
              acl_table.c.object_type,
              acl_table.c.created_at,
              acl_table.c.modified_by_id,
              acl_table.c.updated_at,
              acl_table.c.parent_id,
          ],
          select_statement
      )
  )


def _propagate_to_wf_children(new_wf_acls, child_class):
  """Propagate newly added roles to workflow objects.

  Args:
    wf_new_acl: list of all newly created acl entries for workflows

  Returns:
    list of newly created acl entries for task groups.
  """

  child_table = child_class.__table__
  acl_table = all_models.AccessControlList.__table__
  acr_table = all_models.AccessControlRole.__table__.alias("parent_acr")
  acr_mapped_table = all_models.AccessControlRole.__table__.alias("mapped")

  current_user_id = login.get_current_user_id()

  select_statement = sa.select([
      acl_table.c.person_id,
      acr_mapped_table.c.id,
      child_table.c.id,
      sa.literal(child_class.__name__),
      sa.func.now(),
      sa.literal(current_user_id),
      sa.func.now(),
      acl_table.c.id,
  ]).select_from(
      sa.join(
          sa.join(
              sa.join(
                  child_table,
                  acl_table,
                  sa.and_(
                      acl_table.c.object_id == child_table.c.workflow_id,
                      acl_table.c.object_type == all_models.Workflow.__name__,
                  )
              ),
              acr_table,
          ),
          acr_mapped_table,
          acr_mapped_table.c.name == sa.func.concat(
              acr_table.c.name, " Mapped")
      )
  ).where(
      acl_table.c.id.in_(new_wf_acls)
  )

  _insert_select_acls(select_statement)

  return _get_child_ids(new_wf_acls, child_class)


def _propagate_to_children(new_tg_acls, child_class, id_name, parent_class):
  """Propagate new acls to objects related to task groups

  Args:
    new_tg_acls: list of ids of newly created acl entries for task groups

  Returns:
    list of ids for newy created task group task or task group object entries.
  """

  child_table = child_class.__table__
  acl_table = all_models.AccessControlList.__table__

  current_user_id = login.get_current_user_id()

  parent_id_filed = getattr(child_table.c, id_name)

  select_statement = sa.select([
      acl_table.c.person_id,
      acl_table.c.ac_role_id,
      child_table.c.id,
      sa.literal(child_class.__name__),
      sa.func.now(),
      sa.literal(current_user_id),
      sa.func.now(),
      acl_table.c.id,
  ]).select_from(
      sa.join(
          child_table,
          acl_table,
          sa.and_(
              acl_table.c.object_id == parent_id_filed,
              acl_table.c.object_type == parent_class.__name__,
          )
      )
  ).where(
      acl_table.c.id.in_(new_tg_acls),
  )

  _insert_select_acls(select_statement)

  return _get_child_ids(new_tg_acls, child_class)


def _propagate_to_tgt(new_tg_acls):
  """Propagate ACL entries to task groups tasks.

  Args:
    new_tg_acls: list of propagated ACL ids that belong to task_groups.
  """
  with utils.benchmark("Propagate tg roles to task group tasks"):
    return _propagate_to_children(
        new_tg_acls,
        all_models.TaskGroupTask,
        "task_group_id",
        all_models.TaskGroup,
    )


def _propagate_to_tgo(new_tg_acls):
  """Propagate ACL entries to task groups objects.

  Args:
    new_tg_acls: list of propagated ACL ids that belong to task_groups.
  """
  with utils.benchmark("Propagate tg roles to task group objects"):
    return _propagate_to_children(
        new_tg_acls,
        all_models.TaskGroupObject,
        "task_group_id",
        all_models.TaskGroup,
    )


def _propagate_to_ctg(new_cycle_acls):
  """Propagate ACL entries to cycle task groups and its children.

  Args:
    new_ctg_acls: list of propagated ACL ids that belong to cycles.
  """
  with utils.benchmark("Propagate wf roles to cycles task groups"):
    new_ctg_acls = _propagate_to_children(
        new_cycle_acls,
        all_models.CycleTaskGroup,
        "cycle_id",
        all_models.Cycle,
    )

  _propagate_to_cycle_tasks(new_ctg_acls)


def _propagate_to_cycle_tasks(new_ctg_acls):
  """Propagate ACL roles to cycle tasks and its children.

  Args:
    new_ctg_acls: list of propagated ACL ids that belong to cycle task groups.
  """
  with utils.benchmark("Propagate wf roles to cycles tasks"):
    new_ct_acls = _propagate_to_children(
        new_ctg_acls,
        all_models.CycleTaskGroupObjectTask,
        "cycle_task_group_id",
        all_models.CycleTaskGroup,
    )

  _propagate_to_cte(new_ct_acls)


def _propagate_to_cte(new_ct_acls):
  """Propagate ACL roles from cycle tasks to cycle tasks entries.

  Args:
    new_ct_acls: list of propagated ACL ids that belong to cycle tasks.
  """
  with utils.benchmark("Propagate wf roles to cycles tasks entries"):
    return _propagate_to_children(
        new_ct_acls,
        all_models.CycleTaskEntry,
        "cycle_task_group_object_task_id",
        all_models.CycleTaskGroupObjectTask,
    )


def _propagate_to_tg(new_wf_acls):
  """Propagate workflow ACL roles to task groups and its children.

  Args:
    new_wf_acls: List of ACL ids on a workflow that should be propagated.
  """
  with utils.benchmark("Propagate wf roles to task groups"):
    new_tg_acls = _propagate_to_wf_children(new_wf_acls, all_models.TaskGroup)

  _propagate_to_tgt(new_tg_acls)

  _propagate_to_tgo(new_tg_acls)


def _propagate_to_cycles(new_wf_acls):
  """Propagate workflow ACL roles to cycles and its children.

  Args:
    new_wf_acls: List of ACL ids on a workflow that should be propagated.
  """
  with utils.benchmark("Propagate wf roles to cycles"):
    new_cycle_acls = _propagate_to_wf_children(new_wf_acls, all_models.Cycle)

  _propagate_to_ctg(new_cycle_acls)


def _propagete_new_wf_acls(new_wf_acls):
  """Propagate ACL entries that were added to workflows.

  Args:
    new_wf_acls: List of ACL ids on a workflow that should be propagated.
  """
  with utils.benchmark("Propagate new WF roles to all its children"):
    if not new_wf_acls:
      return

    _propagate_to_tg(new_wf_acls)

    _propagate_to_cycles(new_wf_acls)
