# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from flask import json
from flask import g
from os.path import abspath
from os.path import dirname
from os.path import join

from ggrc.app import app
from integration import ggrc


THIS_ABS_PATH = abspath(dirname(__file__))


class TestCase(ggrc.TestCase):

  CSV_DIR = join(THIS_ABS_PATH, "test_csvs/")

  @classmethod
  def _import_file(cls, filename, dry_run=False):
    data = {"file": (open(join(cls.CSV_DIR, filename)), filename)}
    headers = {
        "X-test-only": "true" if dry_run else "false",
        "X-requested-by": "gGRC",
    }
    if hasattr(g, "cache"):
      delattr(g, "cache")
    tc = app.test_client()
    tc.get("/login")
    response = tc.post("/_service/import_csv", data=data, headers=headers)

    return json.loads(response.data)

  def import_file(self, filename, dry_run=False):
    if dry_run:
      return self._import_file(filename, dry_run=True)
    else:
      response_dry = self._import_file(filename, dry_run=True)
      response = self._import_file(filename)
      self.assertEqual(response_dry, response)
      return response

  def export_csv(self, data):
    headers = {
        'Content-Type': 'application/json',
        "X-requested-by": "gGRC",
        "X-export-view": "blocks",
    }
    return self.client.post("/_service/export_csv", data=json.dumps(data),
                            headers=headers)
