# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"Logical model of dynamic fixtures creation."
# pylint: disable=invalid-name
# pylint: disable=global-variable-not-assigned
# pylint: disable=global-statement

import copy

from lib import factory
from lib.constants import element, objects
from lib.constants.test import batch
from lib.page.widget import info_widget
from lib.service.rest_service import RelationshipsService
from lib.utils import conftest_utils, test_utils


dict_executed_fixtures = {}


def _get_fixture_from_dict_fixtures(fixture):
  """Get value of fixture by key (fixture name) from dictionary of
  executed fixtures."""
  global dict_executed_fixtures
  return {k: v for k, v in dict_executed_fixtures.iteritems()
          if k == fixture}[fixture]


def _new_objs_rest(obj_name, obj_count, is_with_cas):
  """Create new objects via REST API according to object name (plural form),
  objects count and requirements for presence of Custom Attributes.
  Return: [lib.entities.entity.*Entity, ...]
  """
  # pylint: disable=unused-argument
  global dict_executed_fixtures

  def create_objs_rest(name, count):
    """Create new objects via REST API according to object name (plural form)
    and objects count.
    Return: [lib.entities.entity.*Entity, ...]
    """
    return factory.get_cls_rest_service(
        object_name=name)().create_objs(count=count)

  def create_objs_used_parents_rest(name, parent_objs):
    """Create new objects via REST API used parents objects according to object
    name (plural form) and list of parent objects.
    Return: [lib.entities.entity.*Entity, ...]
    """
    return ([factory.get_cls_rest_service(object_name=name)().
            create_objs(count=1,
                        **{parent_obj.type.lower(): parent_obj.__dict__})[0]
             for parent_obj in parent_objs])
  parent_obj_name = None
  if obj_name == objects.AUDITS:
    parent_obj_name = (objects.get_singular(objects.PROGRAMS) if obj_count == 1
                       else objects.PROGRAMS)
  if obj_name in (objects.ASSESSMENT_TEMPLATES, objects.ASSESSMENTS,
                  objects.ISSUES):
    parent_obj_name = (objects.get_singular(objects.AUDITS) if obj_count == 1
                       else objects.AUDITS)
  if parent_obj_name:
    parent_objs = _get_fixture_from_dict_fixtures(
        fixture="new_{}_rest".format(parent_obj_name))
    objs = create_objs_used_parents_rest(
        name=obj_name, parent_objs=parent_objs)
  else:
    objs = create_objs_rest(name=obj_name, count=obj_count)
  return objs


def generate_common_fixtures(*fixtures):  # flake8: noqa
  """Generate, run and return of results for common dynamic fixtures according
  to tuple of fixtures names and used if exist 'web_driver' fixture for UI.
  Examples: fixtures = ('new_program_rest', 'new_controls_rest',
  'map_new_program_rest_to_new_controls_rest', 'new_audit_rest').
  """
  global dict_executed_fixtures

  def new_rest_fixture(fixture):
    """Extract arguments of 'new_rest_fixture' fixture from fixture name,
    create new objects via REST API and return created.
    """
    fixture_params = fixture.replace("new_", "").replace("_rest", "")
    is_with_cas = False
    if "_with_cas" in fixture_params:
      is_with_cas = True
      fixture_params = fixture_params.replace("_with_cas", "")
    obj_name = fixture_params
    obj_count = batch.COUNT
    if objects.get_plural(obj_name) in objects.ALL_OBJS:
      obj_name = objects.get_plural(obj_name)
      obj_count = 1
    new_objs = _new_objs_rest(obj_name, obj_count, is_with_cas)
    return new_objs

  def new_ui_fixture(web_driver, fixture):
    """Extract arguments of 'new_ui_fixture' fixture from fixture name,
    create new objects via UI (LHN) and return UI page object.
    """
    fixture_params = fixture.replace("new_", "").replace("_ui", "")
    obj_name = fixture_params
    obj_count = batch.COUNT
    if (objects.get_plural(obj_name) in objects.ALL_OBJS and
            objects.get_plural(obj_name) != objects.PROGRAMS):
      obj_name = objects.get_plural(obj_name)
      obj_count = 1
      objs_info_pages = [conftest_utils.create_obj_via_lhn(
          web_driver,
          getattr(element.Lhn, obj_name.upper())) for _ in xrange(obj_count)]
      return objs_info_pages
    elif objects.get_plural(obj_name) == objects.PROGRAMS:
      modal = conftest_utils.get_lhn_accordion(
          web_driver,
          getattr(element.Lhn, objects.PROGRAMS.upper())).create_new()
      test_utils.ModalNewPrograms.enter_test_data(modal)
      modal.save_and_close()
      program_info_page = info_widget.Programs(web_driver)
      return modal, program_info_page

  def map_rest_fixture(fixture):
    """Extract arguments of 'map_rest_fixture' fixture from fixture name,
    find previously created source and destination objects,
    map them via REST API and return result of mapping.
    """
    fixture_params = fixture.replace("map_", "")
    _src_obj, _dest_objs = fixture_params.split("_to_")
    src_obj = _get_fixture_from_dict_fixtures(fixture=_src_obj)[0]
    dest_objs = _get_fixture_from_dict_fixtures(fixture=_dest_objs)
    mapped_objs = RelationshipsService().map_objs(
        src_obj=src_obj, dest_objs=dest_objs)
    return mapped_objs

  def update_rest_fixture(fixture):
    """Extract arguments of 'update_rest_fixture' fixture from fixture name,
    update existing objects via REST API and return updated.
    """
    obj_name = fixture.replace("update_", "").replace("_rest", "")
    _objs_to_update = "new_{}_rest".format(obj_name)
    # e.g. need if: 'new_controls_rest' and 'update_control_rest'
    try:
      objs_to_update = _get_fixture_from_dict_fixtures(fixture=_objs_to_update)
    except KeyError:
      _objs_to_update = "new_{}_rest".format(objects.get_plural(obj_name))
      objs_to_update = _get_fixture_from_dict_fixtures(
          fixture=_objs_to_update)[0]
    if objs_to_update:
      if objects.get_plural(obj_name) in objects.ALL_OBJS:
        obj_name = objects.get_plural(obj_name)
      updated_objs = factory.get_cls_rest_service(
          object_name=obj_name)().update_objs(objs=objs_to_update)
      return updated_objs

  def delete_rest_fixture(fixture):
    """Extract arguments of 'delete_rest_fixture' fixture from fixture name,
    delete existing objects via REST API.
    """
    obj_name = fixture.replace("delete_", "").replace("_rest", "")
    _objs_to_delete = "new_{}_rest".format(obj_name)
    # e.g. need if: 'new_controls_rest' and 'delete_control_rest'
    try:
      objs_to_delete = _get_fixture_from_dict_fixtures(fixture=_objs_to_delete)
    except KeyError:
      _objs_to_delete = "new_{}_rest".format(objects.get_plural(obj_name))
      objs_to_delete = _get_fixture_from_dict_fixtures(
          fixture=_objs_to_delete)[0]
    if objs_to_delete:
      if objects.get_plural(obj_name) in objects.ALL_OBJS:
        obj_name = objects.get_plural(obj_name)
      deleted_objs = factory.get_cls_rest_service(
          object_name=obj_name)().delete_objs(objs=objs_to_delete)
      return deleted_objs

  for fixture in fixtures:
    if fixture.startswith("new_") and fixture.endswith("_ui") and dict_executed_fixtures.get("selenium"):
      new_objs = new_ui_fixture(web_driver=dict_executed_fixtures["selenium"], fixture=fixture)
      dict_executed_fixtures.update({fixture: new_objs})
    elif fixture.startswith("new_") and fixture.endswith("_rest"):
      new_objs = new_rest_fixture(fixture=fixture)
      dict_executed_fixtures.update({fixture: new_objs})
    elif (fixture.startswith("map_") and
            fixture.endswith("_rest") and "_to_" in fixture):
      mapped_objs = map_rest_fixture(fixture=fixture)
      dict_executed_fixtures.update({fixture: mapped_objs})
    elif fixture.startswith("update_") and fixture.endswith("_rest"):
      updated_objs = update_rest_fixture(fixture=fixture)
      dict_executed_fixtures.update({fixture: updated_objs})
    elif fixture.startswith("delete_") and fixture.endswith("_rest"):
      deleted_objs = delete_rest_fixture(fixture=fixture)
      dict_executed_fixtures.update({fixture: deleted_objs})
  executed_fixtures_copy = copy.deepcopy(dict_executed_fixtures)
  return executed_fixtures_copy


def generate_snapshots_fixtures(fixture):
  """Generate, run and return of results for snapshots dynamic fixtures
  according to tuple of fixture name.
  Example: 'create_audit_with_control__risk_and_update_control'
           'create_audit_with_controls'
           'create_audit_with_controls_and_update_control'
           'create_audit_with_control__risk_and_update_control__risk
  """
  global dict_executed_fixtures
  if fixture.startswith("create_audit_with_"):
    _creation_params = None
    _action_params = None
    updating_params = []
    deleting_params = []
    fixture_params = fixture.replace("create_audit_with_", "")
    if "_and_" in fixture_params:
      _creation_params, _action_params = fixture_params.split("_and_")
    if "_and_" not in fixture_params:
      _creation_params = fixture_params
    creation_params = ["new_{}_rest".format(param) for param in
                       _creation_params.split("__")]
    mapping_params = [
        "map_new_program_rest_to_new_{}_rest".format(param) for param in
        _creation_params.split("__")]
    creation_part = (["new_program_rest"] + creation_params +
                     mapping_params + ["new_audit_rest"])
    if _action_params:
      if "update" in _action_params:
        updating_params = ["update_{}_rest".format(param) for param in
                           _action_params.replace("update_", "").split("__")]
      if "delete" in _action_params:
        deleting_params = ["delete_{}_rest".format(param) for param in
                           _action_params.replace("delete_", "").split("__")]
    action_part = (updating_params + deleting_params)
    all_manipulations = creation_part + action_part
    generate_common_fixtures(*all_manipulations)
    executed_snapshots_fixtures = copy.deepcopy(dict_executed_fixtures)
    return executed_snapshots_fixtures
