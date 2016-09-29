# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from textwrap import dedent


def title(s, underscore='='):
  return s + '\n' + underscore * len(s)


def doc(descriptor, indent=0):
  if descriptor.doc is None:
    result = dedent("""
        ..  warning::
            Missing doc-string of ``%s``
    """ % descriptor.name).strip()
  else:
    result = descriptor.doc
  return textblock(result, indent)


def textblock(text, indent=0):
  if indent:
    return ('\n' + ' ' * indent).join(text.splitlines())
  return text
