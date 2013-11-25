# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from ggrc import db
from ggrc.app import app
from .mixins import deferred, Base, Stateful
from .types import JsonType
from functools import wraps
from flask import request
from flask.helpers import url_for

class Task(Base, Stateful, db.Model):
  __tablename__ = 'tasks'
  
  VALID_STATES = [
    "Pending",
    "Running",
    "Success",
    "Failure"
  ]
  name = deferred(db.Column(db.String), 'Task')
  parameters = deferred(db.Column(db.PickleType), 'Task')
  result = deferred(db.Column(db.Text), 'Task')
  
  _publish_attrs = [
      'name',
      'result'
  ]
  
  def start(self):
    self.status = "Running"
    
  def finish(self, status, result):
    self.result = result
    self.status = status
    db.session.add(self)
    db.session.commit()
  
def create_task(name, url, parameters):
  from time import time
  task = Task(name = name + str(int(time()))) # task name must be unique
  task.parameters = parameters
  from ggrc.app import db
  db.session.add(task)
  db.session.commit()  

  # schedule a task queue
  from google.appengine.api import taskqueue
  taskqueue = taskqueue.add(url=url, name=task.name, params={'task_id': task.id})
  
  return task

def queued_task(func):
  
  @wraps(func)
  def decorated_view(*args, **kwargs):
    task = Task.query.get(request.form.get("task_id"))
    # task.start()
    try:
      result = func(task)
    except:
      import traceback
      task.finish("Failure", traceback.format_exc())
      # Return 200 so that the task is not retried
      return app.make_response((
        'failure', 200, [('Content-Type', 'text/html')]))
      return result
    
    if isinstance(result, basestring):
      task.finish("Success", result)
    else:
      task.finish("Success", result.response[0])
    return result
  return decorated_view
  