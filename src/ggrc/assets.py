# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com

"""Manage "static" assets

The actual list of stylesheets and javascripts to compile is in 
`assets/assets.yaml`.

When developing, you can use `webassets` to automatically recompile changed
assets by starting the `webassets` command-line utility:

..
  cd src/ggrc
  webassets -m ggrc.assets watch

Currently, Compass/Sass is used to build CSS assets, and it has its own
monitor utility, which can be invoked thusly:

..
  cd src/ggrc
  compass watch -c assets/compass.config.rb
"""

from . import settings

# Initialize webassets to handle the asset pipeline
import webassets

environment = webassets.Environment()

environment.manifest = 'file:assets.manifest'
environment.versions = 'hash:32'

import webassets.updater
environment.updater = webassets.updater.TimestampUpdater()

# Read asset listing from YAML file
import os, yaml, imp
assets_yamls = [os.path.join(settings.MODULE_DIR, 'assets', 'assets.yaml'),]
module_load_paths = [settings.MODULE_DIR,]
for extension in settings.EXTENSIONS:
  file, pathname, description = imp.find_module(extension)
  module_load_paths.append(pathname)
  p = os.path.join(pathname, 'assets', 'assets.yaml')
  if os.path.exists(p):
    assets_yamls.append(p)
asset_paths = {}
for assets_yaml_path in assets_yamls:
  with open(assets_yaml_path) as f:
    for k,v in yaml.load(f.read()).items():
      asset_paths.setdefault(k, []).extend(v)

if not settings.AUTOBUILD_ASSETS:
  environment.auto_build = False

environment.url = '/static'
environment.directory = os.path.join(settings.MODULE_DIR, 'static')

environment.load_path = []
for module_load_path in module_load_paths:
  environment.load_path.extend([
    os.path.join(module_load_path, 'assets/javascripts'),
    os.path.join(module_load_path, 'assets/vendor/javascripts'),
    os.path.join(
      module_load_path,
      'assets/vendor/bootstrap-sass/vendor/assets/javascripts'),
    os.path.join(
      module_load_path, 'assets/vendor/remoteipart/vendor/assets/javascripts'),
    os.path.join(module_load_path, 'assets/stylesheets'),
    os.path.join(module_load_path, 'assets/vendor/stylesheets'),
    os.path.join(module_load_path, 'assets/js_specs'),
    ])

environment.register("dashboard-js", webassets.Bundle(
  *asset_paths['dashboard-js-files'],
  #filters='jsmin',
  output='dashboard-%(version)s.js'))

environment.register("dashboard-css", webassets.Bundle(
  *asset_paths['dashboard-css-files'],
  output='dashboard-%(version)s.css'))

if settings.ENABLE_JASMINE:
  environment.register("dashboard-js-specs", webassets.Bundle(
    *asset_paths['dashboard-js-spec-files'],
    output='dashboard-%(version)s-specs.js'))

  environment.register("dashboard-js-spec-helpers", webassets.Bundle(
    *asset_paths['dashboard-js-spec-helpers'],
    output='dashboard-%(version)s-spec-helpers.js'))
