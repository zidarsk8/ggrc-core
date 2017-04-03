# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for snapshot block converter."""


class SnapshotBlockConverter(object):
  """Block converter for snapshots of a single object type."""

  def __init__(self, converter, ids):
    self.converter = converter
    self.ids = ids

  @staticmethod
  def handle_row_data():
    pass

  @property
  def name(self):
    return "Snapshot"

  @staticmethod
  def to_array():
    return [[]], [[]]  # header and body
