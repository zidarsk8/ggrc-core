# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

import warnings
import sqlalchemy.exc

warnings.simplefilter("error", category=sqlalchemy.exc.SAWarning)
