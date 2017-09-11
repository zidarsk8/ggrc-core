# Copyright (C) 2016 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Custom HTTP error handlers.

Setup is done in ggrc/app.py
"""

from flask import current_app

from ggrc.utils import as_json


def register_handlers(app):
  # pylint: disable=unused-variable; we use bad_request in the decorator
  @app.errorhandler(400)
  def bad_request(err):
    """Custom handler for BadRequest error

    Returns JSON object with error code and message in response body.
    """
    resp = {"code": 400,
            "message": err.description}
    headers = [('Content-Type', 'application/json'), ]
    return current_app.make_response((as_json(resp), 400, headers),)

  @app.errorhandler(401)
  def unauthorized(err):
    """Custom handler for Unauthorized error

    Returns JSON object with error code and message in response body.
    """
    resp = {"code": 401,
            "message": err.description}
    headers = [('Content-Type', 'application/json'), ]
    return current_app.make_response((as_json(resp), 401, headers),)

  @app.errorhandler(404)
  def not_found(err):
    """CUstom handler for NotFound error

    Returns JSON object with error code and message in response body.
    """
    resp = {"code": 404,
            "message": err.description}
    headers = [('Content-Type', 'application/json'), ]
    return current_app.make_response((as_json(resp), 404, headers),)

  @app.errorhandler(500)
  def internal_error(err):
    """CUstom handler for InternalServerError

    Returns JSON object with error code and message in response body.
    """
    resp = {"code": 500,
            "message": err.description}
    headers = [('Content-Type', 'application/json'), ]
    return current_app.make_response((as_json(resp), 500, headers),)
