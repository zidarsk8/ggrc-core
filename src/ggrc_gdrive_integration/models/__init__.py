# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


import ggrc.models.all_models #import all_models,  __all__
from .object_folder import ObjectFolder
from .object_file import ObjectFile
from .object_event import ObjectEvent

ggrc.models.all_models.ObjectFolder = ObjectFolder
ggrc.models.all_models.ObjectFile = ObjectFile
ggrc.models.all_models.ObjectEvent = ObjectEvent
ggrc.models.all_models.ObjectFolder._inflector
ggrc.models.all_models.ObjectFile._inflector
ggrc.models.all_models.ObjectEvent._inflector
ggrc.models.all_models.all_models += [ObjectFolder, ObjectFile, ObjectEvent]
ggrc.models.all_models.__all__ += [ObjectFolder.__name__, ObjectFile.__name__, ObjectEvent.__name__]
