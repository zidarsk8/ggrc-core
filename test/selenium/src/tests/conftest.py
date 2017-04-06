# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""PyTest fixtures."""
# pylint: disable=invalid-name

import pytest

from lib.constants import element
from lib.constants.test import batch
from lib.page.widget import info_widget
from lib.service.rest_service import (
    ProgramsService, AuditsService, ControlsService, IssuesService,
    AssessmentTemplatesService, AssessmentsService, RelationshipsService,
    ObjectsOwnersService)
from lib.utils import conftest_utils, test_utils


# pylint: disable=redefined-outer-name
pytest_plugins = "selenium", "xdist", "xvfb", "timeout", "flask", \
                 "rerunfailures", "timeout", "repeat", "pycharm"


@pytest.yield_fixture(scope="function")
def selenium(selenium):
  """Setup test resources for running test in headless mode."""
  # todo: here we should use selenium.maximize_window() and env variables to
  #  set xvfb resolution in docker container. Setting env vars
  # currently doesn't work for selenium-docker
  selenium.set_window_size(1440, 900)
  yield selenium


@pytest.yield_fixture(scope="function")
def new_control_ui(selenium):
  """Create new Control object via UI (LHN).
  Return: lib.page.widget.Controls
  """
  control_info_page = conftest_utils.create_obj_via_lhn(
      selenium, element.Lhn.CONTROLS)
  yield control_info_page


@pytest.yield_fixture(scope="function")
def new_program_ui(selenium, new_control_ui):
  """Create new Program object via UI (LHN).
  Return: (Program modal, Program Info widget).
  """
  # pylint: disable=redefined-outer-name
  # pylint: disable=unused-argument
  modal = conftest_utils.get_lhn_accordion(
      selenium, element.Lhn.PROGRAMS).create_new()
  test_utils.ModalNewPrograms.enter_test_data(modal)
  modal.save_and_close()
  program_info_page = info_widget.Programs(selenium)
  yield modal, program_info_page


@pytest.yield_fixture(scope="function")
def new_org_group_ui(selenium):
  """Create new Org Group object via UI (LHN).
 Return: lib.page.widget.OrgGroupInfo
 """
  org_group_page = conftest_utils.create_obj_via_lhn(
      selenium, element.Lhn.ORG_GROUPS)
  yield org_group_page


@pytest.yield_fixture(scope="function")
def new_risk_ui(selenium):
  """Create new Risk Group object via UI (LHN).
  Return: lib.page.widget.Risks
  """
  risk_page = conftest_utils.create_obj_via_lhn(
      selenium, element.Lhn.RISKS)
  yield risk_page


@pytest.yield_fixture(scope="function")
def new_issue_ui(selenium):
  """Create new Issue object via UI (LHN).
  Return: lib.page.widget.IssueInfo
  """
  issue_info_page = conftest_utils.create_obj_via_lhn(
      selenium, element.Lhn.ISSUES)
  yield issue_info_page


@pytest.yield_fixture(scope="function")
def new_process_ui(selenium):
  """Create new process object via UI (LHN).
  Return: lib.page.widget.Processes
  """
  process_info_page = conftest_utils.create_obj_via_lhn(
      selenium, element.Lhn.PROCESSES)
  yield process_info_page


@pytest.yield_fixture(scope="function")
def new_data_asset_ui(selenium):
  """Create new Data Asset object via UI (LHN).
  Return: lib.page.widget.DataAssetInfo
  """
  data_asset_page = conftest_utils.create_obj_via_lhn(
      selenium, element.Lhn.DATA_ASSETS)
  yield data_asset_page


@pytest.yield_fixture(scope="function")
def new_system_ui(selenium):
  """Create new System object via UI (LHN).
  Return: lib.page.widget.IssueInfo
  """
  system_page = conftest_utils.create_obj_via_lhn(
      selenium, element.Lhn.SYSTEMS)
  yield system_page


@pytest.yield_fixture(scope="function")
def new_product_ui(selenium):
  """Create new Product object via UI (LHN).
  Return: lib.page.widget.Product
  """
  product_page = conftest_utils.create_obj_via_lhn(
      selenium, element.Lhn.PRODUCTS)
  yield product_page


@pytest.yield_fixture(scope="function")
def new_project_ui(selenium):
  """Create new Project object via UI (LHN).
  Return: lib.page.widget.ProjectInfo
  """
  project_page = conftest_utils.create_obj_via_lhn(
      selenium, element.Lhn.PROJECTS)
  yield project_page


@pytest.yield_fixture(scope="function")
def new_controls_ui(selenium):
  """Create new Controls objects via UI (LHN).
  Return: [lib.page.widget.Controls, ...]
 """
  controls = []
  for _ in xrange(batch.COUNT):
    controls.append(conftest_utils.create_obj_via_lhn(
        selenium, element.Lhn.CONTROLS))
  yield controls


@pytest.yield_fixture(scope="function")
def new_program_rest():
  """Create new Program object via REST API.
  Return: lib.entities.entity.ProgramEntity
  """
  yield ProgramsService().create_objs(count=1)[0]


@pytest.yield_fixture(scope="function")
def new_audit_rest(new_program_rest):
  """Create new Program, Audit objects via REST API.
  Return: (lib.entities.entity.AuditEntity, lib.entities.entity.ProgramEntity)
  """
  yield AuditsService().create_objs(
      count=1, program=new_program_rest.__dict__)[0], new_program_rest


@pytest.yield_fixture(scope="function")
def new_asmt_tmpl_rest(new_audit_rest):
  """Create new Program, Audit, Assessment Template objects via REST API.
  Return:
  (lib.entities.entity.AssessmentTemplateEntity,
  lib.entities.entity.AuditEntity, lib.entities.entity.ProgramEntity)
  """
  yield (AssessmentTemplatesService().
         create_objs(count=1, audit=new_audit_rest[0].__dict__)[0],
         new_audit_rest[0], new_audit_rest[1])


@pytest.yield_fixture(scope="function")
def new_asmt_rest(new_audit_rest):
  """Create new Program, Audit, Assessment objects via REST API.
  Return:
  (lib.entities.entity.AssessmentEntity, lib.entities.entity.AuditEntity,
  lib.entities.entity.ProgramEntity)
  """
  yield (AssessmentsService().
         create_objs(count=1, object=new_audit_rest[1].__dict__,
                     audit=new_audit_rest[0].__dict__)[0],
         new_audit_rest[0], new_audit_rest[1])


@pytest.yield_fixture(scope="function")
def new_issue_rest(new_audit_rest):
  """Create new Program, Audit, Issue objects via REST API.
  Return:
  (lib.entities.entity.IssueEntity, lib.entities.entity.AuditEntity,
  lib.entities.entity.ProgramEntity)
  """
  issue = (IssuesService().create_objs(
      count=1, audit=new_audit_rest[0].__dict__)[0],
      new_audit_rest[0], new_audit_rest[1])
  ObjectsOwnersService().assign_owner_to_objs(objs=issue[0])
  yield issue


@pytest.yield_fixture(scope="function")
def new_control_rest():
  """Create new Control object via REST API.
  Return: lib.entities.entity.ControlEntity
  """
  control = ControlsService().create_objs(count=1)[0]
  ObjectsOwnersService().assign_owner_to_objs(objs=control)
  yield control


@pytest.yield_fixture(scope="function")
def new_controls_rest():
  """Create new Controls objects via REST API.
  Return: [lib.entities.entity.ControlEntity, ...]
  """
  controls = ControlsService().create_objs(count=batch.COUNT)
  ObjectsOwnersService().assign_owner_to_objs(objs=controls)
  yield controls


@pytest.yield_fixture(scope="function")
def update_control_rest(new_control_rest):
  """Update existing Control object via REST API.
  Return: lib.entities.entity.ControlEntity
  """
  yield ControlsService().update_objs(objs=new_control_rest)[0]


@pytest.yield_fixture(scope="function")
def delete_control_rest(new_control_rest):
  """Delete existing Control object via REST API.
  Return: lib.entities.entity.ControlEntity
  """
  yield ControlsService().delete_objs(objs=new_control_rest)


@pytest.yield_fixture(scope="function")
def map_controls_to_program_rest(new_program_rest, new_controls_rest):
  """Create new Program, Controls objects via REST API and map created
  Controls to Program via REST API.
  """
  yield RelationshipsService().map_objs(src_obj=new_program_rest,
                                        dest_objs=new_controls_rest)


@pytest.yield_fixture(scope="function")
def map_control_to_program_rest(new_program_rest, new_control_rest):
  """Create new Program, Control objects via REST API and map created
  Control to Program via REST API.
  """
  yield RelationshipsService().map_objs(src_obj=new_program_rest,
                                        dest_objs=new_control_rest)


@pytest.yield_fixture(scope="function")
def map_issue_to_audit_rest(new_audit_rest, new_issue_rest):
  """Create new Audit (Audit, Program) and new Issue (Issue, Audit, Program)
  objects via REST API and map created Issue to Audit via REST API.
  """
  yield RelationshipsService().map_objs(src_obj=new_issue_rest[0],
                                        dest_objs=new_audit_rest[0])
