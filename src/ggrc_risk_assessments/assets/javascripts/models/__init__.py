# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: laran@reciprocitylabs.com
# Maintained By: laran@reciprocitylabs.com


from ggrc.models.all_models import register_model

from .risk_assessment import RiskAssessment

register_model(RiskAssessment)
