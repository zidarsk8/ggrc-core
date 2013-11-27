# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com

from ggrc import db, settings
from .mixins import deferred, Base, Stateful
from functools import wraps
from flask import request

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
    db.session.add(self)
    db.session.commit()
    
  def finish(self, status, result):
    self.result = result
    self.status = status
    db.session.add(self)
    db.session.commit()

def create_task(name, queued_task, parameters={}):
  from time import time
  task = Task(name = name + str(int(time()))) # task name must be unique
  task.parameters = parameters
  from ggrc.app import db
  db.session.add(task)
  db.session.commit()  

  # schedule a task queue
  if getattr(settings, 'APP_ENGINE', False):
    from google.appengine.api import taskqueue
    from flask import url_for
    cookie_header = [h for h in request.headers if h[0] == 'Cookie']
    taskqueue = taskqueue.add(url=url_for(queued_task.__name__), name=task.name, 
                              params={'task_id': task.id}, 
                              headers = cookie_header)
  else:
    queued_task(task)
  
  return task

def queued_task(func):
  
  @wraps(func)
  def decorated_view(*args, **kwargs):
    if len(args) > 0 and isinstance(args[0], Task):
      task = args[0]
    else:
      task = Task.query.get(request.form.get("task_id"))
    task.start()
    try:
      result = func(task)
    except:
      import traceback
      task.finish("Failure", traceback.format_exc())
      # Return 200 so that the task is not retried
      from ggrc.app import app
      return app.make_response((
        'failure', 200, [('Content-Type', 'text/html')]))
      return result
    
    if isinstance(result, basestring):
      task.finish("Success", result)
    else:
      task.finish("Success", result.response[0])
    return result
  return decorated_view
  
