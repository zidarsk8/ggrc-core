# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from flask import request, current_app

def log_event():
  '''Log javascript client errors to syslog via application logger.'''
  method = request.method.lower()
  if method == 'post':
    severity = request.json['log_event']['severity']
    description = request.json['log_event']['description']
    current_app.logger.error('Javascript Client: %s %s',
        severity, description)
    return current_app.make_response(('', 200, []))
  raise NotImplementedError()
