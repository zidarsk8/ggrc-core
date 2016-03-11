# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""Models for LHN modals when creating new objects"""

from lib.page.modal import base


class Programs(base.ProgramsModal, base.CreateNewObjectModal):
  """Class representing a program modal"""


class Controls(base.ControlsModal, base.CreateNewObjectModal):
  """Class representing a control modal"""


class OrgGroups(base.OrgGroupsModal, base.CreateNewObjectModal):
  """Class representing an org group modal"""


class Risks(base.RisksModal, base.CreateNewObjectModal):
  """Class representing a risk modal"""


class Requests(base.RequestsModal, base.CreateNewObjectModal):
  """Class representing an request modal"""


class Issues(base.IssuesModal, base.CreateNewObjectModal):
  """Class representing an issue modal"""


class Processes(base.ProcessesModal, base.CreateNewObjectModal):
  """Class representing a process modal"""


class DataAssets(base.DataAssetsModal, base.CreateNewObjectModal):
  """Class representing a Data Assets modal"""


class Systems(base.SystemsModal, base.CreateNewObjectModal):
  """Class representing a system modal"""


class Products(base.ProductsModal, base.CreateNewObjectModal):
  """Class representing a product modal"""


class Projects(base.ProjectsModal, base.CreateNewObjectModal):
  """Class representing a process modal"""
