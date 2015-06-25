# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

from collections import defaultdict

from ggrc.converters.import_helper import split_array
from ggrc.converters.base_block import BlockConverter


class Converter(object):

  @classmethod
  def from_csv(cls, dry_run, csv_data):
    converter = Converter(dry_run=dry_run, csv_data=csv_data)
    return converter

  def __init__(self, **kwargs):
    self.dry_run = kwargs.get("dry_run", True)
    self.csv_data = kwargs.get("csv_data", [])
    self.block_converters = []
    self.new_slugs = defaultdict(set)
    self.shared_state = {}

  def import_csv(self):
    self.generate_converters()
    self.import_objects()
    self.gather_new_slugs()
    self.import_mappings()

  def generate_converters(self):
    offsets, data_blocks = split_array(self.csv_data)
    for offset, data in zip(offsets, data_blocks):
      self.block_converters.append(BlockConverter.from_csv(
        data, offset, self.dry_run, self.shared_state))

  def gather_new_slugs(self):
    for converter in self.block_converters:
      object_class, slugs = converter.get_new_slugs()
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
