# Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: andraz@reciprocitylabs.com
# Maintained By: andraz@reciprocitylabs.com


import bleach

from HTMLParser import HTMLParser


# Set up custom tags/attributes for bleach
bleach_tags = [
    'caption', 'strong', 'em', 'b', 'i', 'p', 'code', 'pre', 'tt', 'samp',
    'kbd', 'var', 'sub', 'sup', 'dfn', 'cite', 'big', 'small', 'address',
    'hr', 'br', 'div', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul',
    'ol', 'li', 'dl', 'dt', 'dd', 'abbr', 'acronym', 'a', 'img',
    'blockquote', 'del', 'ins', 'table', 'tbody', 'tr', 'td', 'th',
] + bleach.ALLOWED_TAGS

bleach_attrs = {}

attrs = [
    'href', 'src', 'width', 'height', 'alt', 'cite', 'datetime',
    'title', 'class', 'name', 'xml:lang', 'abbr'
]

for tag in bleach_tags:
  bleach_attrs[tag] = attrs


def cleaner(target, value, oldvalue, initiator):
  # Some cases like Request don't use the title value
  #  and it's nullable, so check for that
  if value is None:
    return value

  parser = HTMLParser()
  value = unicode(value)
  while True:
    lastvalue = value
    value = parser.unescape(
        bleach.clean(value, bleach_tags, bleach_attrs, strip=True)
    )
    if value == lastvalue:
      break
  return value
