# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Resource for handling special endpoints for people."""

import datetime

from werkzeug.exceptions import Forbidden

from ggrc import db
from ggrc.login import get_current_user_id
from ggrc.utils import benchmark
from ggrc.services import common


class PersonResource(common.ExtendedResource):
  """Resource handler for people."""

  # method post is abstract and not used.
  # pylint: disable=abstract-method

  def get(self, *args, **kwargs):
    # This is to extend the get request for additional data.
    # pylint: disable=arguments-differ
    command_map = {
        None: super(PersonResource, self).get,
        "task_count": self._task_count,
    }
    command = kwargs.pop("command", None)
    if command not in command_map:
      self.not_found_response()
    return command_map[command](*args, **kwargs)

  def _task_count(self, id):
    if id != get_current_user_id():
      raise Forbidden()
    with benchmark("Make response"):
      counts_query = db.session.execute(
          """
          SELECT
              overdue,
              sum(task_count)
          FROM (
              SELECT
                  ct.end_date < :today AS overdue,
                  count(ct.id) AS task_count
              FROM cycle_task_group_object_tasks AS ct
              JOIN cycles AS c ON
                  c.id = ct.cycle_id
              WHERE
                  ct.status != "Verified" AND
                  ct.contact_id = :person_id AND
                  c.is_verification_needed = 1 AND
                  c.is_current = 1
              GROUP BY overdue

              UNION ALL

              SELECT
                  ct.end_date < :today AS overdue,
                  count(ct.id) AS task_count
              FROM cycle_task_group_object_tasks AS ct
              JOIN cycles AS c ON
                  c.id = ct.cycle_id
              WHERE
                  ct.status != "Finished" AND
                  ct.contact_id = :person_id AND
                  c.is_verification_needed = 0 AND
                  c.is_current = 1
              GROUP BY overdue
          ) as temp
          GROUP BY overdue
          """,
          {
              # Using today instead of DATE(NOW()) for easier testing with
              # freeze gun.
              "today": datetime.date.today(),
              "person_id": id,
          }
      )
      counts = dict(counts_query.fetchall())
      response_object = {
          "open_task_count": int(sum(counts.values())),
          "has_overdue": bool(counts.get(1, [])),
      }
      return self.json_success_response(response_object, )
