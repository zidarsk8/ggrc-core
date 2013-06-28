# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

def get_extension_name(extension_setting, default):
    from ggrc import settings
    extension_name = getattr(settings, extension_setting, default)
    if extension_name is not None:
      extension_name = extension_name if not callable(extension_name) else \
          extension_name()
    else:
      extension_name = default
    return extension_name

def get_extension_module(extension_setting, default, extension_modules={}):
  if extension_setting not in extension_modules:
    import sys
    extension_name = get_extension_name(extension_setting, default)
    if not extension_name:
      extension_modules[extension_setting] = extension_name
    else:
      __import__(extension_name)
      extension_modules[extension_setting] = sys.modules[extension_name]
  return extension_modules[extension_setting]

def get_extension_instance(extension_setting, default, extensions={}):
  if extension_setting not in extensions:
    import sys
    from ggrc import settings
    extension_name = get_extension_name(extension_setting, default)
    idx = extension_name.rfind('.')
    module_name = extension_name[0:idx]
    class_name = extension_name[idx+1:]
    __import__(module_name)
    module = sys.modules[module_name]
    extensions[extension_setting] = getattr(module, class_name)(settings)
  return extensions[extension_setting]

