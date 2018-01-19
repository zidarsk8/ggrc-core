/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('can.mustache.helper.localize_date', function () {
  'use strict';

  var helper;
  var testDate;
  var fakeOptions;

  beforeAll(function () {
    helper = can.Mustache._helpers.localize_date.fn;
    fakeOptions = {};
  });

  it('returns formatted short ISO format', function () {
    testDate = '2017-01-16';
    expect(helper(testDate, fakeOptions)).toEqual('01/16/2017');
  });

  it('returns formatted full ISO format', function () {
    testDate = '2017-01-16T12:36:20';
    expect(helper(testDate, fakeOptions)).toEqual('01/16/2017');
  });

  it('returns Invalid date for incorrect formats', function () {
    expect(helper('01-01-2017', fakeOptions)).toEqual('Invalid date');
    expect(helper('2017/01/16', fakeOptions)).toEqual('Invalid date');
    expect(helper('01/01/2016', fakeOptions)).toEqual('Invalid date');
    expect(helper('2017-01-16 12:36:20', fakeOptions)).toEqual('Invalid date');
    expect(helper('2017-20-01', fakeOptions)).toEqual('Invalid date');
    expect(helper('01.01.2017', fakeOptions)).toEqual('Invalid date');
  });
});
