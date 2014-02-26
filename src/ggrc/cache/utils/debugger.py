# cache/utils/debugger.py
#
# This module enables interactive python debugger
#
# Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# 
# Maintained By: dan@reciprocitylabs.com
#
import ipdb

def enable_debug():
	ipdb.set_trace()

