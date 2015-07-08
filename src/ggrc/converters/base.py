# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from collections import defaultdict
from itertools import product
from itertools import chain

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

  def to_array(self, data_grid=False):
    self.block_converters_from_ids()
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
      two_empty_lines = [[], []]
      block_data = csv_header + csv_body + two_empty_lines
      [line.insert(0, "") for line in block_data]
      block_data[0][0] = "Object type"
      block_data[1][0] = block_converter.name
      csv_data.extend(block_data)
    return csv_data

  def to_data_grid(self):
    """ multi join datagrid with all objects in one block

    Generate 2d array where each cell represents a cell in a csv file
    """
    grid_blocks = []
    grid_header = []
    for block_converter in self.block_converters:
      csv_header, csv_body = block_converter.to_array()
      grid_header.extend(csv_header[1][:1])
      grid_blocks.append(csv_body)
    grid_data = [list(chain(*i)) for i in product(*grid_blocks)]
    return [grid_header] + grid_data

  def __init__(self, **kwargs):
    self.dry_run = kwargs.get("dry_run", True)
    self.csv_data = kwargs.get("csv_data", [])
    self.ids_by_type = kwargs.get("ids_by_type", [])
    self.block_converters = []
    self.new_slugs = defaultdict(set)
    self.new_emails = set()
    self.shared_state = {}
    self.response_data = []

  def import_csv(self):
    self.block_converters_from_csv()
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

  def block_converters_from_ids(self):
    """ fill the block_converters class variable

    Generate block converters from a list of tuples with an object name and ids
    """
    object_map = {o.__name__: o for o in IMPORTABLE.values()}
    for object_data in self.ids_by_type:
      object_class = object_map[object_data["object_name"]]
      id_list = object_data.get("ids", [])
      fields = object_data.get("fields")
      block_converter = BlockConverter.from_ids(
          self, object_class, ids=id_list, fields=fields)
      block_converter.ids_to_row_converters()
      self.block_converters.append(block_converter)

  def block_converters_from_csv(self):
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
