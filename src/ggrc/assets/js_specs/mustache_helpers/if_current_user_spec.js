/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('can.mustache.helper.if_current_user', function () {
  'use strict';

  var fakeOptions;  // fake mustache options object passed to the helper
  var helper;
  var person;
  var originalUser;

  beforeAll(function () {
    originalUser = GGRC.current_user;
    person = new CMS.Models.Person({
      name: 'Ivan',
      email: 'ivan@example.com',
      type: 'Person',
      id: 42
    });
    GGRC.current_user = person;
    helper = can.Mustache._helpers.if_current_user.fn;
  });

  afterAll(function () {
    GGRC.current_user = originalUser;
  });

  beforeEach(function () {
    fakeOptions = {
      fn: jasmine.createSpy(),
      inverse: jasmine.createSpy(),
      context: {}
    };
  });

  it('triggers rendering of the "truthy" block for value person string',
    function () {
      helper('ivan@example.com', fakeOptions);

      expect(fakeOptions.fn.calls.count()).toEqual(1);
    });

  it('triggers rendering of the "falsy" block for invalid person string',
    function () {
      helper('john@example.com', fakeOptions);

      expect(fakeOptions.inverse.calls.count()).toEqual(1);
    });

  it('triggers rendering of the "truthy" block for person object',
    function () {
      helper(person, fakeOptions);

      expect(fakeOptions.fn.calls.count()).toEqual(1);
    });

  it('triggers rendering of the "falsy" block for empty string',
    function () {
      helper('', fakeOptions);

      expect(fakeOptions.inverse.calls.count()).toEqual(1);
    });

  it('triggers rendering of the "falsy" block for empty object',
    function () {
      spyOn(console, 'warn');
      helper({}, fakeOptions);

      expect(fakeOptions.inverse.calls.count()).toEqual(1);
      expect(console.warn).toHaveBeenCalled();
    });

  it('triggers rendering of the "falsy" block for undefined',
    function () {
      spyOn(console, 'warn');
      helper(undefined, fakeOptions);

      expect(fakeOptions.inverse.calls.count()).toEqual(1);
      expect(console.warn).toHaveBeenCalled();
    });

  it('triggers rendering of the "falsy" block for null',
    function () {
      spyOn(console, 'warn');
      helper(null, fakeOptions);

      expect(fakeOptions.inverse.calls.count()).toEqual(1);
      expect(console.warn).toHaveBeenCalled();
    });
});
