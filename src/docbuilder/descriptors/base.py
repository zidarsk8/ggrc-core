# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from inspect import getdoc
from collections import OrderedDict

from cached_property import cached_property


class DesciptorMeta(type):

  def __init__(cls, name, bases, attrs):
    cls.__registry__ = OrderedDict()
    cls.__registry__.sorted = False
    cls.__registry__.collected = False

  def __contains__(cls, obj):
    return id(obj) in cls.__registry__


class Descriptor(object):

  __metaclass__ = DesciptorMeta

  def __new__(cls, obj):
    oid = id(obj)
    if oid not in cls.__registry__:
      cls.__registry__[oid] = super(Descriptor, cls).__new__(cls, obj)
      cls.__registry__.sorted = False
    return cls.__registry__[oid]

  @classmethod
  def collect(cls):
    raise NotImplementedError('Method should be implemented by subclass')

  @classmethod
  def all(cls):
    if not cls.__registry__.collected:
      for obj in cls.collect():
        cls(obj)
      cls.__registry__.collected = True
    if not cls.__registry__.sorted:
      instances = cls.__registry__.items()
      instances.sort(key=lambda item: item[1].name)
      cls.__registry__.clear()
      cls.__registry__.update(instances)
      cls.__registry__.sorted = True
    return cls.__registry__.itervalues()

  def __init__(self, obj):
    self.obj = obj

  @cached_property
  def name(self):
    try:
      return '%s.%s' % (self.obj.__module__, self.obj.__name__)
    except AttributeError:
      return self.obj.__name__

  @cached_property
  def doc(self):
    return getdoc(self.obj)
