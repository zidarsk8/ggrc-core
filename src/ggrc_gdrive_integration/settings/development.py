# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
import os

EXTENSIONS = ['ggrc_gdrive_integration']
exports = ["GAPI_KEY", "GAPI_CLIENT_ID", "GAPI_ADMIN_GROUP"]

GAPI_KEY = os.environ.get('GGRC_GAPI_KEY', "")
GAPI_CLIENT_ID = os.environ.get('GGRC_GAPI_CLIENT_ID', "")
# Admin group gets writer access to all
GAPI_ADMIN_GROUP = os.environ.get('GGRC_GAPI_ADMIN_GROUP', "")
GAPI_CLIENT_SECRET = os.environ.get('GGRC_GAPI_CLIENT_SECRET', "")
