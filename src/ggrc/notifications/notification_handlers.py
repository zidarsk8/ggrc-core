# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

"""Notification handlers for object in the ggrc module.

This module contains all function needed for handling notification objects
needed by ggrc notifications.
"""

from ggrc.services.common import Resource
from ggrc.models import request
from ggrc.models import assessment


def handle_request_put(sender, obj=None, src=None, service=None):
  pass


def handle_assessment_put(sender, obj=None, src=None, service=None):
  pass


def register_handlers():
  """Register listeners for notification handlers"""

  @Resource.model_put.connect_via(request.Request)
  def request_put_listener(sender, obj=None, src=None, service=None):
    handle_request_put(sender, obj, src, service)

  @Resource.model_put.connect_via(assessment.Assessment)
  def assessment_put_listener(sender, obj=None, src=None, service=None):
    handle_assessment_put(sender, obj, src, service)
