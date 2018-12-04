# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test user permissions loading."""
import mock

from ggrc.models import all_models
from integration.ggrc import TestCase, generator
from integration.ggrc.api_helper import Api
from integration.ggrc.models import factories

from appengine import base


@base.with_memcache
class TestPermissionsLoading(TestCase):
  """Test user permissions loading."""

  def setUp(self):
    super(TestPermissionsLoading, self).setUp()
    self.api = Api()
    self.generator = generator.ObjectGenerator()

    self.control_id = factories.ControlFactory().id

    _, user = self.generator.generate_person(user_role="Creator")
    self.api.set_user(user)

  def test_permissions_loading(self):
    """Test if permissions created only once for GET requests."""
    import ggrc_basic_permissions
    with mock.patch(
        "ggrc_basic_permissions.store_results_into_memcache",
        side_effect=ggrc_basic_permissions.store_results_into_memcache
    ) as store_perm:
      self.api.get(all_models.Control, self.control_id)
      store_perm.assert_called_once()
      store_perm.call_count = 0

      # On second GET permissions should be loaded from memcache
      # but not created from scratch.
      self.api.get(all_models.Control, self.control_id)
      store_perm.assert_not_called()
