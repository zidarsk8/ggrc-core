# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for log_json method."""

from types import NoneType

from ggrc.models import all_models
from integration.ggrc import TestCase
from integration.ggrc.models import factories


class TestLogJson(TestCase):
  """Test checks log_json method."""

  @staticmethod
  def _prepare_create_param(person, list_attr):
    """Method builds params for creating model."""
    create_param = {}
    for attr in list_attr:
      if attr == 'modified_by':
        continue
      create_param[attr] = person
    return create_param

  def _check_json_representation(self, keys_attr, json_representation, model):
    """Result of calling log_json should not contain Model's obj."""
    for item in keys_attr:
      if item in json_representation:
        self.assertTrue(
            isinstance(json_representation[item], (dict, NoneType)),
            msg="Model {} has problem with field {}, after calling "
                "log_json, it == {}"
            .format(model.__name__, item, json_representation[item])
        )

  def test_log_json(self):
    """Test checks work of log_json method for all models"""
    creator_email = "creator@example.com"
    creator = factories.PersonFactory(email=creator_email)
    for model in all_models.all_models:
      attr = [attr for attr in dir(model) if (attr.endswith("_by") and
                                              not attr[0].isupper() and
                                              attr[0] != '_')]
      attr = self._prepare_create_param(creator, attr)
      keys_attr = list(attr.keys())
      if keys_attr:
        try:
          json_representation = model(**attr).log_json()
        except AttributeError:
          continue
        self._check_json_representation(
            keys_attr, json_representation, model
        )
