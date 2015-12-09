# Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: anze@reciprocitylabs.com
# Maintained By: anze@reciprocitylabs.com


from ggrc.models.all_models import register_model

from .risk import Risk
from .risk_object import RiskObject
from .threat import Threat

register_model(Risk)
register_model(RiskObject)
register_model(Threat)
