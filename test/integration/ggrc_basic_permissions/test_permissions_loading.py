# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test user permissions loading and caching."""
import mock

from appengine import base

from ggrc.models import all_models
from ggrc.cache import utils as cache_utils
from integration.ggrc import TestCase, generator
from integration.ggrc.api_helper import Api
from integration.ggrc.models import factories


# stub for module, which cannot be imported in global scope bacause of
# import error
ggrc_basic_permissions = None  # pylint: invalid-name


def _lazy_load_module():
  """Load required module in runtime to prevent import error"""

  global ggrc_basic_permissions  # pylint: global-statement,invalid-name
  import ggrc_basic_permissions  # pylint: disable=redefined-outer-name


@base.with_memcache
class TestMemcacheBase(TestCase):
  """Base class for permissions tests"""

  def setUp(self):
    super(TestMemcacheBase, self).setUp()

    _lazy_load_module()


class TestPermissionsLoading(TestMemcacheBase):
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


class TestPermissionsCacheFlushing(TestMemcacheBase):
  """Test user permissions loading."""

  def setUp(self):
    super(TestPermissionsCacheFlushing, self).setUp()
    self.api = Api()

  @staticmethod
  def load_perms(user_id, new_perms):
    """Emulate procedure to load permissions
    """

    with mock.patch(
        'ggrc_basic_permissions._load_permissions_from_database',
        return_value=new_perms
    ):

      mock_user = mock.Mock()
      mock_user.id = user_id

      return ggrc_basic_permissions.load_permissions_for(mock_user)

  def test_memcache_flushing(self):
    """Test if memcache is properly cleaned on object creation

      Procedure to test functionality:
      1) load and permissions for specific user and store them in memcahe
      2) emulate new object creation, which cleans permissions in memcache
      3) make request which tries to get cache for permissions from memcache

      Also, it's assumed that 2 or more GGRC workers are running
    """

    client = cache_utils.get_cache_manager().cache_object.memcache_client
    client.flush_all()

    # load perms and store them in memcache
    self.load_perms(11, {"11": "a"})

    # emulate situation when a new object is created
    # this procedure cleans memcache in the end
    cache_utils.clear_permission_cache()

    # emulate work of worker #1 - get permissions for our user
    # the first step - check permissions in memcache
    ggrc_basic_permissions.query_memcache(client, "permissions:11")
    # step 2 - load permissions from DB and save then into memcahe
    # this step is omitted

    # load permission on behalf of worker #2, before step 2 of worker #1
    result = self.load_perms(11, {"11": "b"})

    # ensure that new permissions were returned instead of old ones
    self.assertEquals(result, {"11": "b"})

  def test_permissions_flush_on_post(self):
    """Test that permissions in memcache are cleaned after POST request."""
    user = self.create_user_with_role("Creator")
    self.api.set_user(user)
    self.api.client.get("/permissions")

    perm_ids = self.memcache_client.get('permissions:list')
    self.assertEqual(perm_ids, {'permissions:{}'.format(user.id)})

    response = self.api.post(
        all_models.Objective,
        {"objective": {"title": "Test Objective", "context": None}}
    )
    self.assert_status(response, 201)

    perm_ids = self.memcache_client.get('permissions:list')
    self.assertIsNone(perm_ids)

  def test_permissions_flush_on_put(self):
    """Test that permissions in memcache are cleaned after PUT request."""
    with factories.single_commit():
      user = self.create_user_with_role("Creator")
      objective = factories.ObjectiveFactory()
      objective_id = objective.id
      objective.add_person_with_role_name(user, "Admin")

    self.api.set_user(user)
    self.api.client.get("/permissions")

    perm_ids = self.memcache_client.get('permissions:list')
    self.assertEqual(perm_ids, {'permissions:{}'.format(user.id)})

    objective = all_models.Objective.query.get(objective_id)
    response = self.api.put(objective, {"title": "new title"})
    self.assert200(response)

    perm_ids = self.memcache_client.get('permissions:list')
    self.assertIsNone(perm_ids)

  def test_permissions_flush_on_delete(self):
    """Test that permissions in memcache are cleaned after DELETE request."""
    with factories.single_commit():
      user = self.create_user_with_role("Creator")
      objective = factories.ObjectiveFactory()
      objective.add_person_with_role_name(user, "Admin")
      objective_id = objective.id

    self.api.set_user(user)
    self.api.client.get("/permissions")

    perm_ids = self.memcache_client.get('permissions:list')
    self.assertEqual(perm_ids, {'permissions:{}'.format(user.id)})

    objective = all_models.Objective.query.get(objective_id)
    response = self.api.delete(objective)
    self.assert200(response)

    perm_ids = self.memcache_client.get('permissions:list')
    self.assertIsNone(perm_ids)
