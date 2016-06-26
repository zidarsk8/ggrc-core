# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from sqlalchemy import and_

from ggrc import db
from ggrc.models import AssessmentTemplate
from ggrc.models import Person
from ggrc.converters import errors
from ggrc.converters.handlers import handlers

class AssessorColumnHandler(handlers.ColumnHandler):
  pass

class VerifierColumnHandler(handlers.ColumnHandler):
  pass
