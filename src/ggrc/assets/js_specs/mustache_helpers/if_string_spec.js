/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

describe('can.mustache.helper.if_string', function () {
  'use strict';

  var fakeOptions;  // fake mustache options object passed to the helper
  var helper;
  var someContext;

  beforeAll(function () {
    helper = can.Mustache._helpers.if_string.fn;
  });

  beforeEach(function () {
    someContext = {foo: 'bar'};

    fakeOptions = {
      fn: jasmine.createSpy(),
      inverse: jasmine.createSpy(),
      context: someContext
    };
  });

  it('triggers rendering of the "truthy" block for string arguments',
    function () {
      var callArgs;
      var expectedArgs = [someContext];

      helper('this is a string', fakeOptions);

      expect(fakeOptions.fn.calls.count()).toEqual(1);
      callArgs = fakeOptions.fn.calls.mostRecent().args;
      expect(callArgs).toEqual(expectedArgs);
    }
  );

  it('triggers rendering of the inverse block for non-string arguments',
    function () {
      var callArgs;
      var expectedArgs = [someContext];
      var params = [
        ['not', 'a', 'string'],
        {isString: false},
        1234,
        function foo() {}
      ];

      params.forEach(function (param) {
        fakeOptions.inverse.calls.reset();

        helper(param, fakeOptions);

        expect(fakeOptions.inverse.calls.count()).toEqual(1);
        callArgs = fakeOptions.inverse.calls.mostRecent().args;
        expect(callArgs).toEqual(expectedArgs);
      });
    }
  );

  it('raises an error on missing arguments', function () {
    expect(function () {
      helper(fakeOptions);
    }).toThrow(new Error('Invalid number of arguments (0), expected 1.'));
  });

  it('raises an error on too many arguments', function () {
    expect(function () {
      helper('argument 1', 'argument 2', fakeOptions);
    }).toThrow(new Error('Invalid number of arguments (2), expected 1.'));
  });
});
