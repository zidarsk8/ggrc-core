/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import * as issueTrackerUtils from '../../plugins/utils/issue-tracker-utils';

describe('can.Model.Mixin.auditIssueTracker', () => {
  let Mixin;

  beforeAll(function () {
    GGRC.ISSUE_TRACKER_ENABLED = true;
    Mixin = CMS.Models.Mixins.auditIssueTracker;
  });

  describe('initIssueTracker() method', () => {
    let method;

    beforeAll(() => {
      method = Mixin.prototype.initIssueTracker;
      GGRC.ISSUE_TRACKER_ENABLED = false;
    });

    it('should show issue tracker on audit if globally enabled and'+
       ' turn off by default', () => {
      GGRC.ISSUE_TRACKER_ENABLED = true;
      const auditStub = new can.Map({
        type: 'Audit',
      });

      spyOn(issueTrackerUtils, 'initIssueTrackerObject');
      method.apply(auditStub);

      expect(issueTrackerUtils.initIssueTrackerObject.calls.count()).toEqual(1);
      const callArgs = issueTrackerUtils.initIssueTrackerObject
        .calls.mostRecent().args;

      expect(callArgs[1].enabled).toEqual(false); // turn off by default
      expect(callArgs[2]).toEqual(true); // show issue tracker controls
    });

    it('should hide issue tracker on audit if globally disabled and'+
       ' turn off by default', () => {
      GGRC.ISSUE_TRACKER_ENABLED = false;
      const auditStub = new can.Map({
        type: 'Audit',
      });
      spyOn(issueTrackerUtils, 'initIssueTrackerObject');
      method.apply(auditStub);

      expect(issueTrackerUtils.initIssueTrackerObject.calls.count()).toEqual(0);
      expect(auditStub.attr('issue_tracker.enabled')).toBeFalsy();
    });
  });
});
