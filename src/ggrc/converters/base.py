# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from collections import defaultdict

from ggrc.converters import IMPORTABLE
from ggrc.converters.import_helper import split_array
from ggrc.converters.base_block import BlockConverter


class Converter(object):

  class_order = [
      "Person",
      "Program",
      "Audit",
      "Policy",
      "Regulation",
      "Standard",
      "Section",
      "Control",
      "ControlAssessment",
  ]

  @classmethod
  def from_csv(cls, dry_run, csv_data):
    converter = Converter(dry_run=dry_run, csv_data=csv_data)
    return converter

  @classmethod
  def from_ids(cls, data):
    """ generate converter form list of objects and ids

    Args:
      data (list of tuples): List containing tuples with object_name and
                             a list of ids for that object
    """
    object_map = {o.__name__: o for o in IMPORTABLE.values()}
    converter = Converter()
    for object_data in data:
      object_class = object_map[object_data["object_name"]]
      id_list = object_data.get("ids", [])
      fields = object_data.get("fields")
      block_converter = BlockConverter.from_ids(
          converter, object_class, ids=id_list, fields=fields)
      block_converter.ids_to_row_converters()
      converter.block_converters.append(block_converter)

    return converter

  def to_array(self, data_grid=False):
    if data_grid:
      return self.to_data_grid()
    return self.to_block_array()

  def to_block_array(self):
    """ exporting each in it's own block separated by empty lines

    Generate 2d array where each cell represents a cell in a csv file
    """
    csv_data = []
    for block_converter in self.block_converters:
      csv_header, csv_body = block_converter.to_array()
      # multi block csv must have first column empty
      [line.insert(0, "") for line in csv_body]
      two_empty_lines = [[], []]
      csv_data.extend(csv_header + csv_body + two_empty_lines)
    return csv_data

  def to_data_grid(self):
    """ multi join datagrid with all objects in one block

    Generate 2d array where each cell represents a cell in a csv file
    """
    grid_body = []
    grid_header = []
    for block_converter in self.block_converters:
      csv_header, csv_body = block_converter.to_array()
      [line.pop(0) for line in csv_header]
    return grid_header + grid_body

  def __init__(self, **kwargs):
    self.dry_run = kwargs.get("dry_run", True)
    self.csv_data = kwargs.get("csv_data", [])
    self.block_converters = []
    self.new_slugs = defaultdict(set)
    self.new_emails = set()
    self.shared_state = {}
    self.response_data = []

  def import_csv(self):
    self.generate_converters()
    self.handle_priority_blocks()
    self.generate_row_converters()
    self.import_objects()
    self.gather_new_slugs()
    self.import_mappings()

  def handle_priority_blocks(self):
    self.handle_person_blocks()

  def handle_person_blocks(self):
    while (self.block_converters and
           self.block_converters[0].object_class.__name__ == "Person"):
      person_converter = self.block_converters.pop(0)
      person_converter.generate_row_converters()
      person_converter.import_objects()
      _, self.new_emails = person_converter.get_new_values("email")
      self.response_data.append(person_converter.get_info())

  def generate_row_converters(self):
    for converter in self.block_converters:
      converter.generate_row_converters()

  def generate_converters(self):
    offsets, data_blocks = split_array(self.csv_data)
    for offset, data in zip(offsets, data_blocks):
      converter = BlockConverter.from_csv(self, data, offset)
      self.block_converters.append(converter)

    order = defaultdict(lambda: len(self.class_order))
    order.update({c: i for i, c in enumerate(self.class_order)})
    self.block_converters.sort(key=lambda x: order[x.name])

  def gather_new_slugs(self):
    for converter in self.block_converters:
      object_class, slugs = converter.get_new_values("slug")
      self.new_slugs[object_class].update(slugs)

  def import_objects(self):
    for converter in self.block_converters:
      converter.import_objects()

  def import_mappings(self):
    for converter in self.block_converters:
      converter.import_mappings(self.new_slugs)

  def get_info(self):
    for converter in self.block_converters:
      converter.import_mappings(self.new_slugs)
      self.response_data.append(converter.get_info())
    return self.response_data

  def get_object_names(self):
    return [c.object_class.__name__ for c in self.block_converters]
