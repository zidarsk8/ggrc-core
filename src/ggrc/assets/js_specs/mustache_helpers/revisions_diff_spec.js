/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

describe('can.mustache.helper.revisions_diff', function () {
  'use strict';

  var fakeOptions;  // fake mustache options object passed to the helper
  var fakeRevHistory;
  var helper;
  var instance;  // an object the helper retrieves an attribute value from

  beforeAll(function () {
    helper = can.Mustache._helpers.revisions_diff.fn;

    fakeOptions = {
      fn: jasmine.createSpy(),
      contexts: {
        add: jasmine.createSpy().and.callFake(function (newContext) {
          return newContext;
        })
      }
    };

    GGRC.model_attr_defs = {};
  });

  beforeEach(function () {
    instance = new can.Map({});

    instance.get_mapping = jasmine.createSpy().and.callFake(
      function (mappingName) {
        if (mappingName !== 'revision_history') {
          throw new Error('Unknown mapping ' + mappingName);
        }
        return fakeRevHistory;
      }
    );

    fakeRevHistory = [];
  });

  afterEach(function () {
    fakeOptions.fn.calls.reset();
    fakeOptions.contexts.add.calls.reset();
  });

  it('computes an empty list on empty Revision history', function () {
    var callArgs;
    var diffList;

    fakeRevHistory = [];
    helper(instance, fakeOptions);

    expect(fakeOptions.fn.calls.count()).toEqual(1);
    callArgs = fakeOptions.fn.calls.mostRecent().args;

    expect(callArgs.length).toEqual(1);
    diffList = callArgs[0].objectChanges;
    expect(diffList).toEqual([]);
  });

  it('computes an empty list on missing Revision content data', function () {
    var callArgs;
    var diffList;

    fakeRevHistory = [
      {
        instance: {content: undefined}
      },
      {
        instance: {content: undefined}
      }
    ];

    helper(instance, fakeOptions);

    expect(fakeOptions.fn.calls.count()).toEqual(1);
    callArgs = fakeOptions.fn.calls.mostRecent().args;

    expect(callArgs.length).toEqual(1);
    diffList = callArgs[0].objectChanges;
    expect(diffList).toEqual([]);
  });

  it('includes the modification time in the diff object', function () {
    var callArgs;
    var diffList;

    fakeRevHistory = [
      {
        instance: {
          updated_at: '2016-01-24T10:05:42',
          modified_by: {id: 1},
          content: {}
        }
      },
      {
        instance: {
          updated_at: '2016-01-30T08:15:11',
          modified_by: {id: 1},
          content: {}
        }
      }
    ];

    helper(instance, fakeOptions);

    expect(fakeOptions.fn.calls.count()).toEqual(1);
    callArgs = fakeOptions.fn.calls.mostRecent().args;
    expect(callArgs.length).toEqual(1);

    diffList = callArgs[0].objectChanges;
    expect(diffList.length).toEqual(1);
    expect(diffList[0].updatedAt).toEqual('2016-01-30T08:15:11');
  });

  it('includes the author of the change(s) in the diff object', function () {
    var callArgs;
    var diffList;

    fakeRevHistory = [
      {
        instance: {
          updated_at: '2016-01-24T10:05:42',
          modified_by: {id: 1},
          content: {}
        }
      },
      {
        instance: {
          updated_at: '2016-01-30T08:15:11',
          modified_by: {id: 7},
          content: {}
        }
      }
    ];

    helper(instance, fakeOptions);

    expect(fakeOptions.fn.calls.count()).toEqual(1);
    callArgs = fakeOptions.fn.calls.mostRecent().args;
    expect(callArgs.length).toEqual(1);

    diffList = callArgs[0].objectChanges;
    expect(diffList.length).toEqual(1);
    expect(diffList[0].madeBy).toEqual('User 7');
  });

  it('computes diff objects for all successive Revision pairs', function () {
    var actual;
    var expected;
    var callArgs;
    var diffList;

    fakeRevHistory = [
      {
        instance: {
          updated_at: '2016-01-24T10:05:42',
          modified_by: {id: 1},
          content: {
            title: 'Audit 1',
            description: 'first Audit',
            status: 'New'
          }
        }
      },
      {
        instance: {
          updated_at: '2016-01-25T16:36:29',
          modified_by: {id: 5},
          content: {
            title: 'Audit 1.0',
            description: 'This is first audit',
            status: 'New'
          }
        }
      },
      {
        instance: {
          updated_at: '2016-01-30T13:22:59',
          modified_by: {id: 5},
          content: {
            title: 'Audit 1.0',
            description: 'This is first audit',
            status: 'In Progress'
          }
        }
      }
    ];

    helper(instance, fakeOptions);

    expect(fakeOptions.fn.calls.count()).toEqual(1);
    callArgs = fakeOptions.fn.calls.mostRecent().args;
    expect(callArgs.length).toEqual(1);

    diffList = callArgs[0].objectChanges;
    expect(diffList.length).toEqual(2);

    // NOTE: the actual order of the changed fields does not matter,
    // thus the sorting of the list before the assertion
    actual = _.sortBy(diffList[0].changes, 'fieldName');
    expected = [
      {
        fieldName: 'description',
        origVal: 'first Audit',
        newVal: 'This is first audit'
      },
      {
        fieldName: 'title',
        origVal: 'Audit 1',
        newVal: 'Audit 1.0'
      }
    ];
    expect(actual).toEqual(expected);

    // check the 2nd diff object, too
    actual = _.sortBy(diffList[1].changes, 'fieldName');
    expected = [
      {
        fieldName: 'status',
        origVal: 'New',
        newVal: 'In Progress'
      }
    ];
    expect(expected).toEqual(expected);
  });
});
