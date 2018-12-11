# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Provides an HTML cleaner function with sqalchemy compatible API"""
import HTMLParser

import bleach


# Set up custom tags/attributes for bleach
BLEACH_TAGS = [
    'caption', 'strong', 'em', 'b', 'i', 'p', 'code', 'pre', 'tt', 'samp',
    'kbd', 'var', 'sub', 'sup', 'dfn', 'cite', 'big', 'small', 'address',
    'hr', 'br', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul',
    'ol', 'li', 'dl', 'dt', 'dd', 'abbr', 'acronym', 'a', 'img',
    'blockquote', 'del', 'ins', 'table', 'tbody', 'tr', 'td', 'th',
] + bleach.ALLOWED_TAGS

BLEACH_ATTRS = {}

ATTRS = [
    'href', 'src', 'width', 'height', 'alt', 'cite', 'datetime',
    'title', 'class', 'name', 'xml:lang', 'abbr'
]

for tag in BLEACH_TAGS:
  BLEACH_ATTRS[tag] = ATTRS


CLEANER = bleach.sanitizer.Cleaner(
    tags=BLEACH_TAGS, attributes=BLEACH_ATTRS, strip=True
)

PARSER = HTMLParser.HTMLParser()


def cleaner(dummy, value, *_):
  """Cleans out unsafe HTML tags.

  Uses bleach and unescape until it reaches a fix point.

  Args:
    dummy: unused, sqalchemy will pass in the model class
    value: html (string) to be cleaned
  Returns:
    Html (string) without unsafe tags.
  """
  if value is None:
    # No point in sanitizing None values
    return value

  if not isinstance(value, basestring):
    # No point in sanitizing non-strings
    return value

  value = unicode(value)
  while True:
    lastvalue = value
    value = PARSER.unescape(CLEANER.clean(value))
    if value == lastvalue:
      break
  return value
