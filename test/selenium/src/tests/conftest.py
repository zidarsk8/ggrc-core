# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""PyTest fixtures."""
# pylint: disable=invalid-name
# pylint: disable=global-variable-not-assigned
# pylint: disable=unused-argument

import pytest

from lib import dynamic_fixtures


# pylint: disable=redefined-outer-name
pytest_plugins = "selenium", "xdist", "xvfb", "timeout", "flask", \
                 "rerunfailures", "timeout", "repeat", "pycharm"


def _common_fixtures(request):
  """Generate common fixtures and return global dictionary of executed
  common fixtures.
  """
  dynamic_fixtures.generate_common_fixtures(request.fixturename)
  return dynamic_fixtures.dict_executed_fixtures[request.fixturename]


@pytest.yield_fixture(scope="function")
def selenium(selenium):
  """Create Web Driver instance and setup test resources for running test
  in headless mode.
  """
  selenium.set_window_size(1440, 900)
  dynamic_fixtures.dict_executed_fixtures.update({"selenium": selenium})
  yield selenium


@pytest.yield_fixture(scope="function")
def new_program_ui(selenium, request):
  """Create new Program object via UI (LHN).
  Return: (Program modal, Program Info widget).
  """
  yield _common_fixtures(request)


@pytest.yield_fixture(scope="function")
def new_org_group_ui(selenium, request):
  """Create new Org Group object via UI (LHN).
  Return: lib.page.widget.OrgGroupInfo
  """
  yield _common_fixtures(request)[0]


@pytest.yield_fixture(scope="function")
def new_risk_ui(selenium, request):
  """Create new Risk Group object via UI (LHN).
  Return: lib.page.widget.Risks
  """
  yield _common_fixtures(request)[0]


@pytest.yield_fixture(scope="function")
def new_program_rest(request):
  """Create new Program object via REST API.
  Return: lib.entities.entity.ProgramEntity
  """
  yield _common_fixtures(request)[0]


@pytest.yield_fixture(scope="function")
def new_control_rest(request):
  """Create new Control object via REST API.
  Return: lib.entities.entity.ControlEntity
  """
  yield _common_fixtures(request)[0]


@pytest.yield_fixture(scope="function")
def new_controls_rest(request):
  """Create new Controls objects via REST API.
  Return: [lib.entities.entity.ControlEntity, ...]
  """
  yield _common_fixtures(request)


@pytest.yield_fixture(scope="function")
def new_audit_rest(request):
  """Create new Audit under Program object via REST API.
  Return: lib.entities.entity.AuditEntity
  """
  yield _common_fixtures(request)[0]


@pytest.yield_fixture(scope="function")
def new_assessment_rest(request):
  """Create new Assessment under Audit object via REST API.
  Return: lib.entities.entity.AssessmentEntity
  """
  yield _common_fixtures(request)[0]


@pytest.yield_fixture(scope="function")
def new_issue_rest(request):
  """Create new Issue under Audit object via REST API.
  Return: lib.entities.entity.IssueEntity
  """
  yield _common_fixtures(request)[0]


@pytest.yield_fixture(scope="function")
def new_assessment_template_rest(request):
  """Create new Assessment Template under Audit object via REST API.
  Return: lib.entities.entity.AssessmentTemplateEntity
  """
  yield _common_fixtures(request)[0]


@pytest.yield_fixture(scope="function")
def map_new_program_rest_to_new_control_rest(request):
  """Map Control to Program object via REST API return response from server.
  """
  yield _common_fixtures(request)


@pytest.yield_fixture(scope="function")
def map_new_program_rest_to_new_controls_rest(request):
  """Map Controls to Program object via REST API return response from server.
  """
  yield _common_fixtures(request)


def _snapshots_fixtures(request):
  """Generate snapshot fixtures used generation of common fixtures and return
  dictionary of executed common fixtures in scope of snapshot fixtures.
  """
  return dynamic_fixtures.generate_snapshots_fixtures(request.fixturename)


@pytest.yield_fixture(scope="function")
def create_audit_with_control(request):
  """Create Program and Control, map Control to Program, create Audit
  under Program via REST API and return dictionary of executed fixtures.
  """
  yield _snapshots_fixtures(request)


@pytest.yield_fixture(scope="function")
def create_audit_with_control_and_update_control(request):
  """Create Program and Control, map Control to Program, create Audit
  under Program, update Control via REST API and return dictionary of executed
  fixtures.
  """
  yield _snapshots_fixtures(request)


@pytest.yield_fixture(scope="function")
def create_audit_with_control_and_delete_control(request):
  """Create Program and Control, map Control to Program, create Audit
  under Program, delete Control via REST API and return dictionary of executed
  fixtures.
  """
  yield _snapshots_fixtures(request)
