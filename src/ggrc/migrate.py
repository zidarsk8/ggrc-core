# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

import os.path
import sys
from alembic.config import Config
from alembic.environment import EnvironmentContext
from alembic.script import ScriptDirectory
from ggrc import settings

class ExtensionPackageEnv(object):
  def __init__(self, extension_module):
    self.extension_module = extension_module
    self.config = make_extension_config(self.extension_module)
    self.script_dir = ScriptDirectory.from_config(self.config)

  def run_env(self, fn, **kwargs):
    with EnvironmentContext(
        self.config,
        self.script_dir,
        fn=fn,
        version_table=extension_version_table(self.extension_module),
        **kwargs):
      self.script_dir.run_env()

def get_extension_dir(module):
  return os.path.dirname(os.path.abspath(module.__file__))

def get_extension_migrations_dir(module):
  return os.path.join(
      get_extension_dir(module),
      'migrations',
      )

def get_base_migrations_dir():
  import ggrc
  return os.path.join(
      os.path.dirname(os.path.dirname(os.path.abspath(ggrc.__file__))),
      'migrations',
      )

def get_base_config_file():
  return os.path.join(get_base_migrations_dir(), 'alembic.ini')

def make_extension_config(module):
  config = Config(get_base_config_file())
  config.set_main_option(
      'script_location',
      get_extension_migrations_dir(module),
      )
  config.set_main_option(
      'sqlalchemy.url',
      settings.SQLALCHEMY_DATABASE_URI,
      )
  return config

def extension_version_table(module):
  return '{0}_alembic_version'.format(module.__name__)

def get_extension_module(module_name):
  __import__(module_name)
  return sys.modules[module_name]

def extensions_list():
  return [get_extension_module(m) for m in settings.EXTENSIONS]

def extension_migrations_dir(extension_module):
  module_dir = get_extension_dir(extension_module)
  migrations_dir = os.path.join(module_dir, 'migrations')
  if os.path.exists(migrations_dir):
    return migrations_dir
  return None

def extension_migrations_list():
  ret = []
  for extension_module in extensions_list():
    migrations_dir = extension_migrations_dir(extension_module)
    if migrations_dir:
      ret.append(migrations_dir)
  return ret

def upgrade(extension_module_name):
  extension_module = get_extension_module(extension_module_name)
  pkg_env = ExtensionPackageEnv(extension_module)
  revision = pkg_env.script_dir.get_current_head()
  print('Upgrading Extension Module {0}:'.format(extension_module_name))

  def do_upgrade(rev, context):
    if rev == revision:
      print('  - extension module is already up to date.')
      return []
    print('  - upgrading extension module from {0} to {1}...'.format(
        rev, revision))
    return context.script._upgrade_revs(revision, rev)

  pkg_env.run_env(
      do_upgrade,
      starting_rev=None,
      destination_rev=revision,
      )
  print

def upgradeall():
  extension_modules = getattr(settings, 'EXTENSIONS', [])
  for module_name in extension_modules:
    upgrade(module_name)

def main(args):
  if len(args) < 3:
    print 'usage: migrate module_name <alembic command string>'
    return -1
  action = args[2]
  if action == 'upgrade':
    upgrade(args[1])
  elif action == 'upgradeall':
    upgradeall()
  return 0

if __name__ == '__main__':
  main(sys.argv)
