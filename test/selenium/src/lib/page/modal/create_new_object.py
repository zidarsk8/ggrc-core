# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Modals for creating new objects"""

from lib.page.modal import base


class NewProgramModal(base.ProgramModal, base.CreateNewObjectModal):
  """Class representing a program modal visible after creating a new
  program from LHN"""


class NewControlModal(base.ControlModal, base.CreateNewObjectModal):
  """Class representing a control modal visible after creating a new
  control from LHN"""


class NewOrgGroupModal(base.OrgGroupModal, base.CreateNewObjectModal):
  """Class representing an org group modal visible after creating a new
  org group from LHN"""


class NewRiskModal(base.RiskModal, base.CreateNewObjectModal):
  """Class representing a risk modal visible after creating a new
  risk from LHN"""
