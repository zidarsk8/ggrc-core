# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: dan@reciprocitylabs.com
# Maintained By: dan@reciprocitylabs.com


from ggrc import db
from ggrc.models.mixins import deferred, Base, Titled, Described, Timeboxed, Noted
from ggrc.models.object_document import Documentable

class RiskAssessment(Documentable, Timeboxed, Noted, Described, Titled, Base, db.Model):
  __tablename__ = 'risk_assessments'

  gdrive_evidence_folder = deferred(db.Column(db.String), 'RiskAssessment')
  ra_manager_id = deferred(db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False), 'RiskAssessment')
  ra_counsel_id = deferred(db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False), 'RiskAssessment')
  

  _fulltext_attrs = [
    'name',
    'description',
    'notes',
    ]

  _publish_attrs = [
    'name',
    'ra_manager',
    'ra_counsel',
    'description',
    'notes',
    ]
