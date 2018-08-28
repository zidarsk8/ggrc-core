# Copyright (C) 2018 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Risk Assessment module"""

from flask import Blueprint

# Initialize Flask Blueprint for extension
blueprint = Blueprint(
    'risk_assessments',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/ggrc_risk_assessments',
)
