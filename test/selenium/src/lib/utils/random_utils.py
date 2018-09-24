# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Generate random stuff."""
from datetime import datetime
import random
import string

from lib import users


def get_title(obj_type):
  """Returns a random title for object with type `obj_type`."""
  return "{}_{}_{}".format(obj_type, _current_time(), get_string())


def get_email(domain=users.DEFAULT_EMAIL_DOMAIN):
  """Returns a random email with domain `domain`."""
  return "{}{}@{}".format(get_string(), _current_time(), domain)


STANDARD_CHARS = string.ascii_letters + string.punctuation + string.digits
# Part of string after `<` is removed (GGRC-6037)
STANDARD_CHARS = STANDARD_CHARS.replace("<", "")


def _current_time():
  """Returns current time, to be included into strings in order to check when
  they were created.
  """
  return datetime.now().strftime("%H%M%S.%f")[:-3]


def get_string(size=15, chars=STANDARD_CHARS):
  """Returns string of size `size` that consists of characters `chars`.
  """
  return "".join(random.choice(chars) for _ in range(size))
