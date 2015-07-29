# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: miha@reciprocitylabs.com
# Maintained By: miha@reciprocitylabs.com

import re

def pretty_name(name):
  """ Add spaces to camel case strings """
  return " ".join(re.findall('[A-Z][^A-Z]*', name))
