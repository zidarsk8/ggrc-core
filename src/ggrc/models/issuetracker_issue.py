
import logging

from ggrc import db
from ggrc.models.mixins import Base

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class IssuetrackerIssue(Base, db.Model):
  """Class representing IssuetrackerIssue."""

  __tablename__ = 'issuetracker_issues'

  object_id = db.Column(db.Integer, nullable=False)
  object_type = db.Column(db.String, nullable=False)

  enabled = db.Column(db.Boolean, nullable=False, default=False)

  component_id = db.Column(db.String(50), nullable=False)
  hotlist_id = db.Column(db.String(50), nullable=True)
  issue_type = db.Column(db.String(50), nullable=False)
  issue_priority = db.Column(db.String(50), nullable=False)
  issue_severity = db.Column(db.String(50), nullable=False)

  issue_id = db.Column(db.String(50), nullable=True)
  issue_url = db.Column(db.String(50), nullable=True)

  _MANDATORY_ATTRS = (
      'object_type', 'object_id', 'component_id',
      'issue_type', 'issue_priority', 'issue_severity',
  )

  @classmethod
  def get_issue(cls, object_type, object_id):
    return cls.query.filter(
        cls.object_type == object_type,
        cls.object_id == object_id).first()

  @classmethod
  def _validate_info(cls, info):
    missing_attrs = [
        attr
        for attr in cls._MANDATORY_ATTRS
        if attr not in info
    ]
    if missing_attrs:
      raise ValueError(
          'Issue tracker info is missing mandatory attributes: %s' % (
              ', '.join(missing_attrs)))


  def to_dict(self, include_issue=False):
    res = {
        'enabled': self.enabled,
        'component_id': self.component_id,
        'hotlist_id': self.hotlist_id,
        'issue_type': self.issue_type,
        'issue_priority': self.issue_priority,
        'issue_severity': self.issue_severity,
    }
    if include_issue:
      res['issue_id'] = self.issue_id
      res['issue_url'] = self.issue_url

    return res

  @classmethod
  def create_from_dict(cls, info):
    logger.info('---> IssuetrackerIssue.create_from_dict: %s', info)
    cls._validate_info(info)
    return cls(
        object_type=info['object_type'],
        object_id=info['object_id'],
        enabled=bool(info.get('enabled')),
        component_id=info['component_id'],

        hotlist_id=info.get('hotlist_id'),

        issue_type=info['issue_type'],
        issue_priority=info['issue_priority'],
        issue_severity=info['issue_severity'],

        issue_id=info.get('issue_id'),
        issue_url=info.get('issue_url'),
    )

  def update_from_dict(self, info):
    logger.info('---> IssuetrackerIssue.update_from_dict: %s', info)
    self._validate_info(info)
    self.object_type = info['object_type']
    self.object_id = info['object_id']
    self.enabled = info['enabled']
    self.component_id = info['component_id']

    self.hotlist_id = info.get('hotlist_id')

    self.issue_type = info['issue_type']
    self.issue_priority = info['issue_priority']
    self.issue_severity = info['issue_severity']

    self.issue_id = info.get('issue_id')
    self.issue_url = info.get('issue_url')
