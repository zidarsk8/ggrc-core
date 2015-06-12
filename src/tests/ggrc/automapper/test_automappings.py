# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

import os
import random

from tests.ggrc import TestCase
from tests.ggrc.generator import GgrcGenerator

from ggrc.models import Regulation, Section, Issue, Relationship

if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestAutomappings(TestCase):

  def setUp(self):
    TestCase.setUp(self)
    self.gen = GgrcGenerator()

  def tearDown(self):
    TestCase.tearDown(self)

  def create_mapping(self, src, dst):
    _, rel = self.gen.generate(Relationship, 'relationship', { 'relationship': {
      'context': None,
      'source': { 'id': src.id, 'type': src.type },
      'destination': { 'id': dst.id, 'type': dst.type }
    }})
    self.assertIsNotNone(rel)

  def test_mapping_to_sections(self):
    _, regulation = self.gen.generate(Regulation, 'regulation', { 'regulation': {
      'context': None,
      'title': 'Test Regulation',
    }})

    _, section = self.gen.generate(Section, 'section', { 'section': {
      'context': None,
      'title': 'Test section',
      'directive': { 'id': regulation.id },
    }})

    _, issue = self.gen.generate(Issue, 'issue', { 'issue': {
      'context': None,
      'title': 'Test issue',
    }})


    self.create_mapping(section, regulation)
    self.create_mapping(issue, section)

    rel = Relationship.find_related(issue, regulation)
    self.assertIsNotNone(rel)

