# Copyright (C) 2019 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""App entities related to control."""
import attr

from lib.app_entity import _base


@attr.s
class Control(_base.Base, _base.WithTitleAndCode):
  """Represents Control entity."""
  admins = attr.ib()
  assertions = attr.ib()
  comments = attr.ib()


@attr.s
class ControlAssertion(_base.Base):
  """Represents control assertion."""
  name = attr.ib()
