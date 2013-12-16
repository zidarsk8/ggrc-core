# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com
import os

DEBUG = True
TESTING = True
HOST = '0.0.0.0'
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:root@127.0.0.1/ggrcdev?charset=utf8'
FULLTEXT_INDEXER = 'ggrc.fulltext.mysql.MysqlIndexer'
LOGIN_MANAGER = 'ggrc.login.noop'
#SQLALCHEMY_ECHO = True
AUTOBUILD_ASSETS = True
ENABLE_JASMINE = True
#DEBUG_ASSETS = True

# Export GAPI for person tooltips
GAPI_KEY = os.environ.get('GGRC_GAPI_KEY', "AIzaSyAndAzs1E-8brJdESH7YSuvrj3A8Y-MZCg")
GAPI_CLIENT_ID = os.environ.get('GGRC_GAPI_CLIENT_ID', "831270113958.apps.googleusercontent.com")
exports = ["GAPI_KEY", "GAPI_CLIENT_ID"]
