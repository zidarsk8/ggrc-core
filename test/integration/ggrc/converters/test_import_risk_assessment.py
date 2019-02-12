# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Tests for Risk Assessment import."""

from collections import OrderedDict
import datetime

import ddt

from ggrc.converters import errors
from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc.models import factories


@ddt.ddt
class TestRiskAssessmentImport(TestCase):
  """Risk Assessment Import Test Class"""

  @ddt.data(
      ("valid_user@example.com,", []),
      ("user2@example.com,\nvalid_user@example.com",
       [errors.MULTIPLE_ASSIGNEES.format(line=3, column_name="Risk Counsel")]),
  )
  @ddt.unpack
  def test_ra_import_counsels(self, counsel, expected_warnings):
    """Tests Risk Counsel for Risk Assessment imported and set correctly"""
    with factories.single_commit():
      program = factories.ProgramFactory()
      risk_assessment = factories.RiskAssessmentFactory(program=program)
      factories.PersonFactory(email="valid_user@example.com")

    data = OrderedDict([
        ("object_type", "RiskAssessment"),
        ("code", risk_assessment.slug),
        ("program", program.slug),
        ("title", "RA-1"),
        ("start date", datetime.date(2018, 10, 22)),
        ("end date", datetime.date(2018, 10, 31)),
        ("risk counsel", counsel),
    ])
    expected_messages = {
        "Risk Assessment": {
            "row_warnings": set(expected_warnings),
        },
    }
    response = self.import_data(data)
    self._check_csv_response(response, expected_messages)
    risk_assessment = all_models.RiskAssessment.query.one()
    self.assertEqual(risk_assessment.ra_counsel.email,
                     "valid_user@example.com")

  @ddt.data(
      (" ;,", []),
      ("user2@example.com;\nuser3@example.com",
       [
           errors.MULTIPLE_ASSIGNEES.format(line=3,
                                            column_name="Risk Counsel"),
           errors.UNKNOWN_USER_WARNING.format(line=3,
                                              email="user2@example.com"),
           errors.UNKNOWN_USER_WARNING.format(line=3,
                                              email="user3@example.com"),
       ]),
  )
  @ddt.unpack
  def test_ra_import_wrong_counsels(self, counsel, expected_warnings):
    """Test import Risk Assessment counsel failed"""
    with factories.single_commit():
      program = factories.ProgramFactory()
      risk_assessment = factories.RiskAssessmentFactory(program=program)
      factories.PersonFactory(email="valid_user@example.com")

    data = OrderedDict([
        ("object_type", "RiskAssessment"),
        ("code", risk_assessment.slug),
        ("program", program.slug),
        ("title", "RA-1"),
        ("start date", datetime.date(2018, 10, 22)),
        ("end date", datetime.date(2018, 10, 31)),
        ("risk counsel", counsel),
    ])

    expected_messages = {
        "Risk Assessment": {
            "row_warnings": set(expected_warnings),
        },
    }
    response = self.import_data(data)
    self._check_csv_response(response, expected_messages)
    risk_assessment = all_models.RiskAssessment.query.one()
    self.assertFalse(risk_assessment.ra_counsel)

  @ddt.data(
      ("valid_user@example.com", []),
      ("user2@example.com\nvalid_user@example.com",
       [errors.MULTIPLE_ASSIGNEES.format(line=3, column_name="Risk Manager")]),
  )
  @ddt.unpack
  def test_ra_import_managers(self, manager, expected_warnings):
    """Tests Risk Manager for Risk Assessment imported and set correctly"""

    with factories.single_commit():
      program = factories.ProgramFactory()
      risk_assessment = factories.RiskAssessmentFactory(program=program)
      factories.PersonFactory(email="valid_user@example.com")

    data = OrderedDict([
        ("object_type", "RiskAssessment"),
        ("code", risk_assessment.slug),
        ("program", program.slug),
        ("title", "RA-1"),
        ("start date", datetime.date(2018, 10, 22)),
        ("end date", datetime.date(2018, 10, 31)),
        ("risk manager", manager),
    ])

    expected_messages = {
        "Risk Assessment": {
            "row_warnings": set(expected_warnings),
        },
    }
    response = self.import_data(data)
    self._check_csv_response(response, expected_messages)
    risk_assessment = all_models.RiskAssessment.query.one()
    self.assertEqual(risk_assessment.ra_manager.email,
                     "valid_user@example.com")

  @ddt.data(
      ("", []),
      ("user2@example.com\nuser3@example.com", [
          errors.MULTIPLE_ASSIGNEES.format(line=3,
                                           column_name="Risk Manager"),
          errors.UNKNOWN_USER_WARNING.format(line=3,
                                             email="user2@example.com"),
          errors.UNKNOWN_USER_WARNING.format(line=3,
                                             email="user3@example.com"),
      ]),
  )
  @ddt.unpack
  def test_ra_import_wrong_managers(self, manager, expected_warnings):
    """Test import Risk Assessment manager failed"""

    with factories.single_commit():
      program = factories.ProgramFactory()
      risk_assessment = factories.RiskAssessmentFactory(program=program)
      factories.PersonFactory(email="valid_user@example.com")

    data = OrderedDict([
        ("object_type", "RiskAssessment"),
        ("code", risk_assessment.slug),
        ("program", program.slug),
        ("title", "RA-1"),
        ("start date", datetime.date(2018, 10, 22)),
        ("end date", datetime.date(2018, 10, 31)),
        ("risk manager", manager),
    ])

    expected_messages = {
        "Risk Assessment": {
            "row_warnings": set(expected_warnings),
        },
    }
    response = self.import_data(data)
    self._check_csv_response(response, expected_messages)
    risk_assessment = all_models.RiskAssessment.query.one()
    self.assertFalse(risk_assessment.ra_manager)
