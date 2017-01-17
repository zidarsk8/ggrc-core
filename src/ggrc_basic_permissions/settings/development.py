# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

EXTENSIONS = ['ggrc_basic_permissions']
USER_PERMISSIONS_PROVIDER = 'ggrc_basic_permissions.CompletePermissionsProvider'

import os
BOOTSTRAP_ADMIN_USERS = \
  os.environ.get('GGRC_BOOTSTRAP_ADMIN_USERS', '').split(' ')
