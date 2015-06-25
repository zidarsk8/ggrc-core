# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com

import os
import random
import itertools

from tests.ggrc import TestCase
from tests.ggrc.generator import GgrcGenerator

from ggrc.models import (Regulation, Section, Relationship, 
                         Program, Control, Objective)
from ggrc import db
from ggrc.automapper.rules import rules


if os.environ.get('TRAVIS', False):
  random.seed(1)  # so we can reproduce the tests if needed


counter = 0


def next(msg):
  global counter
  counter += 1
  return msg + str(counter)


class automapping_count_limit:
  def __init__(self, new_limit):
    self.new_limit = new_limit

  def __enter__(self):
    self.original_limit = rules.count_limit
    rules.count_limit = self.new_limit

  def __exit__(self, type, value, traceback):
    rules.count_limit = self.original_limit


class TestAutomappings(TestCase):

  def setUp(self):
    TestCase.setUp(self)
    self.gen = GgrcGenerator()

  def tearDown(self):
    TestCase.tearDown(self)

  def create_object(self, cls, data):
    name = cls.__name__.lower()
    data['context'] = None
    res, obj = self.gen.generate(cls, name, {name: data})
    self.assertIsNotNone(obj, '%s, %s: %s' % (name, str(data), str(res)))
    return obj

  def create_mapping(self, src, dst):
    return self.create_object(Relationship, {
        'source': {'id': src.id, 'type': src.type},
        'destination': {'id': dst.id, 'type': dst.type}
    })

  def assert_mapping(self, obj1, obj2, missing=False):
    db.session.flush()
    rel = Relationship.find_related(obj1, obj2)
    if not missing:
      self.assertIsNotNone(rel,
                           msg='%s not mapped to %s' % (obj1.type, obj2.type))
    else:
      self.assertIsNone(rel,
                        msg='%s mapped to %s' % (obj1.type, obj2.type))

  def assert_mapping_implication(self, to_create, implied):
    objects = set()
    mappings = set()
    relate = lambda src, dst: (src, dst) if src < dst else (dst, src)
    if type(to_create) is not list:
      to_create = [to_create]
    for src, dst in to_create:
      objects.add(src)
      objects.add(dst)
      self.create_mapping(src, dst)
      mappings.add(relate(src, dst))
    if type(implied) is not list:
      implied = [implied]
    for src, dst in implied:
      objects.add(src)
      objects.add(dst)
      self.assert_mapping(src, dst)
      mappings.add(relate(src, dst))
    possible = set()
    for src, dst in itertools.product(objects, objects):
      possible.add(relate(src, dst))
    for src, dst in possible - mappings:
      self.assert_mapping(src, dst, missing=True)

  def with_permutations(self, mk1, mk2, mk3):
    obj1, obj2, obj3 = mk1(), mk2(), mk3()
    self.assert_mapping_implication(
        to_create=[(obj1, obj2), (obj2, obj3)],
        implied=(obj1, obj3),
    )
    obj1, obj2, obj3 = mk1(), mk2(), mk3()
    self.assert_mapping_implication(
        to_create=[(obj2, obj3), (obj1, obj2)],
        implied=(obj1, obj3),
    )

  def test_mapping_directive_to_a_program(self):
    self.with_permutations(
        lambda: self.create_object(Program, {'title': next('Program')}),
        lambda: self.create_object(Regulation, {
            'title': next('Test PD Regulation')
        }),
        lambda: self.create_object(Objective, {'title': next('Objective')}),
    )

  def test_mapping_to_sections(self):
    regulation = self.create_object(Regulation, {
        'title': next('Test Regulation')
    })
    section = self.create_object(Section, {
        'title': next('Test section'),
        'directive': {'id': regulation.id},
    })
    objective = self.create_object(Objective, {'title': next('Objective')})

    self.assert_mapping_implication(
        to_create=(objective, section),
        implied=(objective, regulation),
    )

  def test_automapping_limit(self):
    with automapping_count_limit(-1):
      program = self.create_object(Program, {'title': next('Program')})
      regulation = self.create_object(Regulation, {
          'title': next('Test PD Regulation')
      })
      objective = self.create_object(Objective, {'title': next('Objective')})
      self.assert_mapping_implication(
          to_create=[(regulation, objective), (objective, program)],
          implied=[],
      )

  def test_mapping_to_objective(self):
    regulation = self.create_object(Regulation, {
        'title': next('Test PD Regulation')
    })
    section = self.create_object(Section, {
        'title': next('Test section'),
        'directive': {'id': regulation.id},
    })
    control = self.create_object(Control, {'title': next('Test control')})
    objective = self.create_object(Objective, {'title': next('Test control')})

    self.assert_mapping_implication(
        to_create=[(section, objective), (objective, control)],
        implied=[
            (regulation, objective),
            (section, control),
            (regulation, control),
        ]
    )

  def test_mapping_between_objectives(self):
    regulation = self.create_object(Regulation, {
        'title': next('Test PD Regulation')
    })
    section = self.create_object(Section, {
        'title': next('Test section'),
        'directive': {'id': regulation.id},
    })
    objective1 = self.create_object(Objective, {'title': next('Test Objective')})
    objective2 = self.create_object(Objective, {'title': next('Test Objective')})

    self.assert_mapping_implication(
        to_create=[(section, objective1), (objective1, objective2)],
        implied=[
            (section, objective2),
            (regulation, objective1),
            (regulation, objective2),
        ]
    )
