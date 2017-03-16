/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('can.mustache.helper.is_overdue', function () {
  'use strict';

  var fakeOptions;  // fake mustache options object passed to the helper
  var helper;
  var templateContext;

  beforeAll(function () {
    helper = can.Mustache._helpers.is_overdue.fn;
  });

  beforeEach(function () {
    templateContext = {foo: 'bar'};

    fakeOptions = {
      fn: jasmine.createSpy(),
      inverse: jasmine.createSpy(),
      contexts: templateContext,
      hash: {
        next_date: '2010-04-02'
      }
    };
  });

  it('triggers rendering of "truthy" block when status is passed', function () {
    var callArgs;
    var expectedArgs = [templateContext];

    helper('2010-01-01', 'Fake Status', fakeOptions);

    expect(fakeOptions.fn.calls.count()).toEqual(1);
    callArgs = fakeOptions.fn.calls.mostRecent().args;
    expect(callArgs).toEqual(expectedArgs);
  });

  it('triggers rendering of "falsy" block when status is passed', function () {
    var callArgs;
    var expectedArgs = [templateContext];
    fakeOptions.hash = undefined;

    helper('2030-01-01', 'Fake Status', fakeOptions);

    expect(fakeOptions.inverse.calls.count()).toEqual(1);
    callArgs = fakeOptions.inverse.calls.mostRecent().args;
    expect(callArgs).toEqual(expectedArgs);
  });

  it('triggers "truthy" block rendering when no status passed', function () {
    var callArgs;
    var expectedArgs = [templateContext];

    helper('2010-01-01', fakeOptions);

    expect(fakeOptions.fn.calls.count()).toEqual(1);
    callArgs = fakeOptions.fn.calls.mostRecent().args;
    expect(callArgs).toEqual(expectedArgs);
  });

  it('triggers "falsy" block rendering when status is "Verified"', function () {
    var callArgs;
    var expectedArgs = [templateContext];

    helper('2010-01-01', 'Verified', fakeOptions);

    expect(fakeOptions.inverse.calls.count()).toEqual(1);
    callArgs = fakeOptions.inverse.calls.mostRecent().args;
    expect(callArgs).toEqual(expectedArgs);
  });
});
