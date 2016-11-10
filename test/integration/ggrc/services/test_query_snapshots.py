# coding: utf-8

# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for /query api endpoint."""

from datetime import datetime
from operator import itemgetter
from flask import json
from nose.plugins.skip import SkipTest

from ggrc import db
from ggrc import views
from ggrc.models import CustomAttributeDefinition as CAD

from integration.ggrc.converters import TestCase
from integration.ggrc.models import factories


class BaseQueryAPITestCase(TestCase):
  """Base class for /query api tests with utility methods."""

  def setUp(self):
    """Log in before performing queries."""
    # we don't call super as TestCase.setUp clears the DB
    # super(BaseQueryAPITestCase, self).setUp()
    self.client.get("/login")

  def _setup_objects(self):
    audit = factories.AuditFactory()
    factories.MarketFactory()
    factories.MarketFactory()


  def test_basic_query_in(self):
    """Filter by ~ operator."""
    self._setup_objects()
