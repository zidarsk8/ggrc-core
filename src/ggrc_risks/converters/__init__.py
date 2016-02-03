# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


""" Module for handling import and export of all risk models """

from ggrc_risks import models

IMPORTABLE = {
    "risk": models.Risk,
    "threat": models.Threat,
}
