# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: mouli@meics.org
# Maintained By: dan@reciprocitylabs.com


from datetime import timedelta
from datetime import datetime
from math import floor

from flask import current_app, request
from sqlalchemy import inspect

import ggrc_workflows.models as models
from ggrc.services.common import Resource
from ggrc.models import NotificationConfig
from ggrc_basic_permissions.models import Role, UserRole
from ggrc import db
from ggrc import settings
from ggrc.login import get_current_user



