/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanModel from 'can-model/src/can-model';
import CanMap from 'can-map/can-map';

describe('validateIssueTracker extension', () => {
  let TestModel;

  beforeAll(() => {
    TestModel = CanModel.extend({}, {
      define: {
        issue_tracker: {
          value: {},
          validate: {
            validateIssueTracker: true,
          },
        },
      },
    });
  });

  it('should return TRUE. issue tracker is disabled', () => {
    const instance = new TestModel();
    instance.attr('issue_tracker', new CanMap({
      enabled: false,
    }));
    expect(instance.validate()).toBeTruthy();
    expect(instance.errors.issue_tracker).toBeUndefined();
  });

  it('should return TRUE. issue tracker is empty object', () => {
    const instance = new TestModel();
    instance.attr('issue_tracker', {});
    expect(instance.validate()).toBeTruthy();
    expect(instance.errors.issue_tracker).toBeUndefined();
  });

  it('should return TRUE. issue tracker has component id', () => {
    const instance = new TestModel();
    instance.attr('issue_tracker', new CanMap({
      enabled: true,
      component_id: 12345,
    }));
    expect(instance.validate()).toBeTruthy();
    expect(instance.errors.issue_tracker).toBeUndefined();
  });

  it('should return FALSE. issue tracker does not have component id', () => {
    const instance = new TestModel();
    instance.attr('issue_tracker', new CanMap({
      enabled: true,
    }));
    expect(instance.validate()).toBeFalsy();
    expect(instance.errors.issue_tracker[0].component_id)
      .toEqual('cannot be blank');
  });
});
