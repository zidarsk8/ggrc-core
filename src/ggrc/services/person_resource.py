# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Resource for handling special endpoints for people."""

import datetime

from ggrc import db
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
    with benchmark("Make response"):
      counts_query = db.session.execute(
          """
          SELECT
              ct.end_date < :today AS overdue,
              count(ct.id) AS task_count
          FROM cycle_task_group_object_tasks AS ct
          JOIN cycles AS c
              ON c.id = ct.cycle_id
          JOIN access_control_list AS acl
              ON acl.object_id = ct.id
              AND acl.object_type = "CycleTaskGroupObjectTask"
          JOIN access_control_roles as acr
              ON acl.ac_role_id = acr.id
          WHERE
              ct.status != "Verified"
              AND c.is_current = 1
              AND acl.person_id = :person_id
              AND acr.name = "Task Assignees"
              -- not needed on non_editable role that has read rights:
              -- acr.read = 1
          GROUP BY overdue;
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
          "open_task_count": sum(counts.values()),
          "has_overdue": bool(counts.get(1, [])),
      }
      return self.json_success_response(response_object, )
