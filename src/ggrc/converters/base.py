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
    converter = Converter()
    for object_name, ids in data.items():
      object_type = IMPORTABLE[object_name]
      converter.block_converters.append(
          BlockConverter.from_ids(converter, object_type, ids))
    return converter

  def to_array(self):
    csv_data = []
    for block_converter in self.block_converters:
      csv_data.extend(block_converter.to_array())
    return csv_data

  def __init__(self, **kwargs):
    self.dry_run = kwargs.get("dry_run", True)
    self.csv_data = kwargs.get("csv_data", [])
    self.block_converters = []
    self.new_slugs = defaultdict(set)
    self.new_emails = set()
    self.shared_state = {}

  def import_csv(self):
    self.generate_converters()
    self.generate_row_converters()
    self.import_objects()
    self.gather_new_slugs()
    self.gather_new_emails()
    self.import_mappings()

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

  def gather_new_emails(self):
    if self.block_converters[0].object_class.__name__ == "Person":
      _, self.new_emails = self.block_converters[0].get_new_values("email")


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
    response_data = []
    for converter in self.block_converters:
      converter.import_mappings(self.new_slugs)
      response_data.append(converter.get_info())
    return response_data
