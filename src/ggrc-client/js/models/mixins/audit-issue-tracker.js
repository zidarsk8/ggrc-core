/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';
import * as issueTrackerUtils from '../../plugins/utils/issue-tracker-utils';

const AUDIT_ISSUE_TRACKER = {
  hotlist_id: '766459',
  component_id: '188208',
  issue_severity: 'S2',
  issue_priority: 'P2',
  issue_type: 'PROCESS',
};

export default Mixin('auditIssueTracker',
  issueTrackerUtils.issueTrackerStaticFields,
  {
    'after:init'() {
      this.initIssueTracker();
    },
    'before:refresh'() {
      issueTrackerUtils.cleanUpWarnings(this);
    },
    'after:refresh'() {
      this.initIssueTracker();
    },
    initIssueTracker() {
      if (!GGRC.ISSUE_TRACKER_ENABLED) {
        return;
      }

      if (!this.issue_tracker) {
        this.attr('issue_tracker', new can.Map({}));
      }

      let auditIssueTracker = new can.Map(AUDIT_ISSUE_TRACKER).attr({
        enabled: false, // turned OFF by default for AUDIT
      });
      issueTrackerUtils.initIssueTrackerObject(
        this,
        auditIssueTracker,
        true
      );
    },
    issueTrackerEnabled() {
      return issueTrackerUtils.isIssueTrackerEnabled(this);
    },
  },
);
