# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

import os
import random

from tests.ggrc import TestCase
from tests.ggrc.generator import GgrcGenerator

from ggrc.models import Regulation, Section, Issue, Relationship, Program
from ggrc import db

if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed


class TestAutomappings(TestCase):

  def setUp(self):
    TestCase.setUp(self)
    self.gen = GgrcGenerator()

  def tearDown(self):
    TestCase.tearDown(self)

  def create_object(self, cls, data):
    name = cls.__name__.lower()
    data['context'] = None
    _, obj = self.gen.generate(cls, name, {name: data})
    self.assertIsNotNone(obj)
    return obj

  def create_mapping(self, src, dst):
    return self.create_object(Relationship, {
        'source': {'id': src.id, 'type': src.type},
        'destination': {'id': dst.id, 'type': dst.type}
    })

  def assert_mapping(self, obj1, obj2):
    db.session.flush()
    rel = Relationship.find_related(obj1, obj2)
    self.assertIsNotNone(rel)

  def test_mapping_to_a_program(self):
    program = self.create_object(Program, {'title': 'Program1'})
    issue = self.create_object(Issue, {'title': 'Issue2'})
    regulation = self.create_object(Regulation, {
        'title': 'Program Regulation'
    })
    self.create_mapping(program, regulation)
    self.create_mapping(issue, program)
    self.assert_mapping(issue, regulation)

  def test_mapping_directive_to_a_program(self):
    regulation = self.create_object(Regulation, {
        'title': 'Test PD Regulation'
    })
    issue = self.create_object(Issue, {'title': 'Issue3'})
    program = self.create_object(Program, {'title': 'Program3'})
    self.create_mapping(regulation, issue)
    self.create_mapping(program, regulation)
    self.assert_mapping(program, issue)

  def test_mapping_to_sections(self):
    regulation = self.create_object(Regulation, {'title': 'Test Regulation'})
    section = self.create_object(Section, {
        'title': 'Test section',
        'directive': {'id': regulation.id},
    })
    issue = self.create_object(Issue, {'title': 'Test issue'})

    self.create_mapping(issue, section)
    self.assert_mapping(issue, regulation)

