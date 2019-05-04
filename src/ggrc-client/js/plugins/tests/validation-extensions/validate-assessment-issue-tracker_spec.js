/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanModel from 'can-model/src/can-model';
import CanMap from 'can-map/can-map';

describe('validateAssessmentIssueTracker extension', () => {
  let TestModel;

  beforeAll(() => {
    TestModel = CanModel.extend({}, {
      define: {
        issue_tracker: {
          value: {},
          validate: {
            validateAssessmentIssueTracker: true,
          },
        },
        can_use_issue_tracker: {
          value: true,
        },
      },
    });
  });

  it('should return FALSE. issue tracker does not have component id', () => {
    const instance = new TestModel();
    instance.attr('issue_tracker', new CanMap({
      enabled: true,
    }));
    instance.attr('can_use_issue_tracker', true);
    expect(instance.validate()).toBeFalsy();
    expect(instance.errors.issue_tracker[0].component_id)
      .toEqual('cannot be blank');
  });

  it('should return TRUE. issue tracker has component id', () => {
    const instance = new TestModel();
    instance.attr('issue_tracker', new CanMap({
      enabled: true,
      component_id: 1,
    }));
    instance.attr('can_use_issue_tracker', true);
    expect(instance.validate()).toBeTruthy();
    expect(instance.errors.issue_tracker).toBeUndefined();
  });

  it('should return TRUE. can_use_issue_tracker - true, enabled - false',
    () => {
      const instance = new TestModel();
      instance.attr('issue_tracker', new CanMap({
        enabled: false,
      }));
      instance.attr('can_use_issue_tracker', true);
      expect(instance.validate()).toBeTruthy();
      expect(instance.errors.issue_tracker).toBeUndefined();
    }
  );

  it('should return TRUE. can_use_issue_tracker - false, enabled - false',
    () => {
      const instance = new TestModel();
      instance.attr('issue_tracker', new CanMap({
        enabled: false,
      }));
      instance.attr('can_use_issue_tracker', false);
      expect(instance.validate()).toBeTruthy();
      expect(instance.errors.issue_tracker).toBeUndefined();
    }
  );
});
