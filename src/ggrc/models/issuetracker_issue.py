
import logging

from ggrc import db
from ggrc.models.mixins import Base

logger = logging.getLogger(__name__)  # pylint: disable=invalid-name


class IssuetrackerIssue(Base, db.Model):
  """Class representing IssuetrackerIssue."""

  __tablename__ = 'issuetracker_issues'

  object_id = db.Column(db.Integer, nullable=False)
  object_type = db.Column(db.String(250), nullable=False)

  enabled = db.Column(db.Boolean, nullable=False, default=False)

  title = db.Column(db.String(250), nullable=False)
  component_id = db.Column(db.String(50), nullable=False)
  hotlist_id = db.Column(db.String(50), nullable=True)
  issue_type = db.Column(db.String(50), nullable=False)
  issue_priority = db.Column(db.String(50), nullable=False)
  issue_severity = db.Column(db.String(50), nullable=False)
  assignee = db.Column(db.String(250), nullable=True)
  cc_list = db.Column(db.Text, nullable=True)

  issue_id = db.Column(db.String(50), nullable=True)
  issue_url = db.Column(db.String(250), nullable=True)

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


  def to_dict(self, include_issue=False, include_private=None):
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
      res['title'] =  self.title

    if include_private:
      res['object_id'] = self.object_id
      res['object_type'] = self.object_type
      res['assignee'] = self.assignee
      res['cc_list'] = self.cc_list.split(',') if self.cc_list else []

    return res

  @classmethod
  def create_or_update_from_dict(cls, object_type, object_id, info):
    if not info:
      raise ValueError('Issue tracker info cannot be empty.')

    issue_obj = cls.get_issue(object_type, object_id)

    info = dict(info, object_type=object_type, object_id=object_id)
    if issue_obj is not None:
      logger.info('------> [CREATE/UPDATE] update issue object')
      issue_obj.update_from_dict(info)
    else:
      logger.info('------> [CREATE/UPDATE] create issue object')
      issue_obj = cls.create_from_dict(info)
      db.session.add(issue_obj)

    return issue_obj

  @classmethod
  def create_from_dict(cls, info):
    logger.info('---> IssuetrackerIssue.create_from_dict: %s', info)
    cls._validate_info(info)

    cc_list = info.get('cc_list')
    if cc_list is not None:
      cc_list = ','.join(cc_list)

    return cls(
        object_type=info['object_type'],
        object_id=info['object_id'],
        enabled=bool(info.get('enabled')),
        title=info.get('title'),
        component_id=info['component_id'],

        hotlist_id=info.get('hotlist_id'),

        issue_type=info['issue_type'],
        issue_priority=info['issue_priority'],
        issue_severity=info['issue_severity'],
        assignee=info.get('assignee'),
        cc_list=cc_list,

        issue_id=info.get('issue_id'),
        issue_url=info.get('issue_url'),
    )

  def update_from_dict(self, info):
    logger.info('---> IssuetrackerIssue.update_from_dict: %s', info)

    cc_list = info.pop('cc_list', None)

    info = dict(
        self.to_dict(include_issue=True, include_private=True),
        **info)

    if cc_list is not None:
      info['cc_list'] = cc_list

    if info['cc_list'] is not None:
      info['cc_list'] = ','.join(info['cc_list'])

    self.object_type = info['object_type']
    self.object_id = info['object_id']
    self.enabled = info['enabled']
    self.title = info['title']
    self.component_id = info['component_id']

    self.hotlist_id = info['hotlist_id']

    self.issue_type = info['issue_type']
    self.issue_priority = info['issue_priority']
    self.issue_severity = info['issue_severity']
    self.assignee = info['assignee']
    self.cc_list = info['cc_list']

    self.issue_id = info['issue_id']
    self.issue_url = info['issue_url']
