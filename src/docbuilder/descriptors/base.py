# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from textwrap import dedent

from cached_property import cached_property


class DesciptorMeta(type):

  def __init__(cls, name, bases, attrs):
    cls.__registry__ = {}
    cls.__cache__ = None
    cls.__built__ = False

  def __contains__(cls, obj):
    return id(obj) in cls.__registry__


class Descriptor(object):

  __metaclass__ = DesciptorMeta

  def __new__(cls, obj):
    oid = id(obj)
    if oid not in cls.__registry__:
      cls.__registry__[oid] = super(Descriptor, cls).__new__(cls, obj)
      cls.__cache__ = None
    return cls.__registry__[oid]

  @classmethod
  def collect(cls):
    raise NotImplementedError('Method should be implemented by subclass')

  @classmethod
  def build(cls):
    if cls.__built__:
      return
    cls.__built__ = True
    try:
      objects = cls.collect()
    except NotImplementedError:
      return
    for obj in objects:
      cls(obj)

  @classmethod
  def all(cls):
    cls.build()
    if not cls.__cache__:
      cls.__cache__ = cls.__registry__.values()
      cls.__cache__.sort()
    return iter(cls.__cache__)

  def __init__(self, obj):
    self.obj = obj

  def __cmp__(self, other):
    return cmp(self.name, other.name)

  @cached_property
  def name(self):
    try:
      return '%s.%s' % (self.obj.__module__, self.obj.__name__)
    except AttributeError:
      return self.obj.__name__

  @cached_property
  def doc(self):
    result = self.obj.__doc__
    if result is None:
      return None
    result = result.strip()
    if '\n' not in result:
      return result
    title, body = result.split('\n', 1)
    title = title.strip()
    body = dedent(body).strip()
    return title + '\n\n' + body
