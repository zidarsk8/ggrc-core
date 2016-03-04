# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: jernej@reciprocitylabs.com
# Maintained By: jernej@reciprocitylabs.com

"""All smoke tests relevant to people/groups page"""
# pylint: disable=no-self-use
# pylint: disable=invalid-name

import pytest    # pylint: disable=import-error
from lib import base
from lib.constants import url


class TestOrgGroupPage(base.Test):
  """Tests the org group page, a part of smoke tests, section 7."""

  @pytest.mark.smoke_tests
  def test_app_redirects_to_new_org_group_page(self, new_org_group):
    """Tests if after saving and closing the lhn_modal the app redirects to
    the object page.

    Generally we start at a random url. Here we verify that after saving
    and closing the lhn_modal we're redirected to an url that contains an
    object id.
    """
    assert url.ORG_GROUPS + "/" + new_org_group.object_id in \
        new_org_group.url
