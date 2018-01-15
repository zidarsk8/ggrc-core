# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""SQLAlchemy hooks for Workflow model."""

from collections import defaultdict
import sqlalchemy as sa
from sqlalchemy.sql.expression import or_, and_

from ggrc import db
from ggrc import login
from ggrc.models import all_models
from ggrc.access_control.role import get_custom_roles_for


RELATED_MODELS = (all_models.TaskGroup, all_models.TaskGroupTask,
                  all_models.Cycle, all_models.CycleTaskGroup,
                  all_models.CycleTaskGroupObjectTask,
                  all_models.CycleTaskEntry)


def init_hook():
  """Initialize hook handler responsible for ACL record creation."""
  sa.event.listen(sa.orm.session.Session, "after_flush", handle_acl_changes)


def handle_acl_changes(session, flush_context):
  """ACL creation hook handler."""
  # pylint: disable=unused-argument
  context = defaultdict(lambda: {
      model: defaultdict(set) for model in RELATED_MODELS
  })
  wf_new_acl = defaultdict(set)
  for obj in session.new:
    if (isinstance(obj, all_models.AccessControlList) and
            obj.object_type == all_models.Workflow.__name__):
      wf_new_acl[obj.object_id].add(obj)
    elif isinstance(obj, RELATED_MODELS):
      workflow = _get_workflow(obj)
      context[workflow.id][obj.__class__][obj.id].update(
          workflow.access_control_list)
  _init_context(wf_new_acl, context)
  create_related_roles(context)

  related_to_del = defaultdict(set)
  for obj in session.deleted:
    if isinstance(obj, RELATED_MODELS):
      related_to_del[obj.type].add(obj.id)
  remove_related_acl(related_to_del)


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

  qfilter = []
  for rtype, ids in related_to_del.iteritems():
    qfilter.append(and_(
        all_models.AccessControlList.object_type == rtype,
        all_models.AccessControlList.object_id.in_(ids)))

  db.session.query(all_models.AccessControlList).filter(or_(*qfilter)).delete(
      synchronize_session='fetch')


def _get_workflow(related_obj):
  """Get workflow from given related object.

  Args:
      related_obj: Workflow's related object

  Returns:
      Workflow instance which contains related_obj.
  """
  if isinstance(related_obj, (all_models.TaskGroup, all_models.Cycle)):
    return related_obj.workflow
  elif isinstance(related_obj, all_models.TaskGroupTask):
    return related_obj.task_group.workflow
  elif isinstance(related_obj, (all_models.CycleTaskGroupObjectTask,
                  all_models.CycleTaskGroup, all_models.CycleTaskEntry)):
    return related_obj.cycle.workflow
  return None


def _add_children_to_context(child_model, foreign_key, parent_wf_map,
                             wf_new_acl, context):
  """Add information about related objects (children) into context.

  Args:
      child_model: related model, for which data should be added into context.
      foreign_key: foreign key which links related and parent models.
      parent_wf_map: contains mapping from parent_id to related workflow_id.
      wf_new_acl: dictionary with mapping workflow_id to set of newly
          created parent ACL records.
      context: dictionary with information for ACL propagation.
  """
  related = db.session.query(
      child_model.id, getattr(child_model, foreign_key)
  ).filter(getattr(child_model, foreign_key).in_(parent_wf_map.keys()))
  for child_id, parent_id in related:
    wf_id = parent_wf_map[parent_id]
    context[wf_id][child_model][child_id].update(wf_new_acl[wf_id])


def _add_parents_to_context(parent_model, wf_new_acl, context):
  """Add information about related objects (parents) into context.

  Args:
      parent_model: related model, for which data should be added into context.
      wf_new_acl: dictionary with mapping workflow_id to set of newly
          created parent ACL records.
      context: dictionary with information for ACL propagation.
  """
  parent_wf_map = {}
  parents = db.session.query(
      parent_model.id, parent_model.workflow_id
  ).filter(parent_model.workflow_id.in_(wf_new_acl.keys()))
  for parent_id, wf_id in parents:
    context[wf_id][parent_model][parent_id].update(wf_new_acl[wf_id])
    parent_wf_map[parent_id] = wf_id
  return parent_wf_map


def _init_context(wf_new_acl, context):
  """Initialize context for newly created parent ACL records propagation.

  Args:
      wf_new_acl: dictionary with mapping workflow_id to set of newly
          created parent ACL records.
      context: dictionary with information for future ACL propagation.
          It consists next data.
          {
            workflow_id: {
              all_models.TaskGroup: {
                id1: set(acl1, acl2, ...),
                ...
              },
              all_models.TaskGroupTask: {
                id1: set(acl1, acl2, ...),
                ...
              },
              all_models.Cycle: {
                id1: set(acl1, acl2, ...),
                ...
              },
              all_models.CycleTaskGroup: {
                id1: set(acl1, acl2, ...),
                ...
              },
              all_models.CycleTaskGroupObjectTask: {
                id1: set(acl1, acl2, ...),
                ...
              },
              all_models.CycleTaskEntry: {
                id1: set(acl1, acl2, ...),
                ...
              },
            },
            ...
          }
  """
  if not wf_new_acl:
    return

  tg_wf_map = _add_parents_to_context(all_models.TaskGroup, wf_new_acl,
                                      context)
  if tg_wf_map:
    _add_children_to_context(all_models.TaskGroupTask, "task_group_id",
                             tg_wf_map, wf_new_acl, context)

  cycle_wf_map = _add_parents_to_context(all_models.Cycle, wf_new_acl, context)
  if cycle_wf_map:
    _add_children_to_context(all_models.CycleTaskGroup, "cycle_id",
                             cycle_wf_map, wf_new_acl, context)

    _add_children_to_context(all_models.CycleTaskGroupObjectTask, "cycle_id",
                             cycle_wf_map, wf_new_acl, context)

    _add_children_to_context(all_models.CycleTaskEntry, "cycle_id",
                             cycle_wf_map, wf_new_acl, context)


def create_related_roles(context):
  """Create related roles for Workflow related objects.

  Args:
      context: dictionary with information for ACL propagation.
  """
  if not context:
    return

  for related in context.values():
    for rel_model, rel_acl_map in related.iteritems():
      for rel_id, acl_set in rel_acl_map.iteritems():
        for p_acl in acl_set:
          rel_person_id = p_acl.person.id if p_acl.person else p_acl.person_id
          custom_roles = get_custom_roles_for(p_acl.object_type)
          parent_acr_id = (p_acl.ac_role.id
                           if p_acl.ac_role else p_acl.ac_role_id)
          parent_acr_name = custom_roles[parent_acr_id]
          rel_acr_name = "{} Mapped".format(parent_acr_name)
          rel_acr_id = next(ind for ind in custom_roles
                            if custom_roles[ind] == rel_acr_name)
          db.session.add(all_models.AccessControlList(
              person_id=rel_person_id,
              ac_role_id=rel_acr_id,
              object_type=rel_model.__name__,
              object_id=rel_id,
              parent=p_acl,
              modified_by_id=login.get_current_user_id(),
          ))
