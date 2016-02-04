/*!
 Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: urban@reciprocitylabs.com
 Maintained By: urban@reciprocitylabs.com
 //*/

describe('can.mustache.helper.date', function () {
  'use strict';

  var helper;
  var instance;

  beforeAll(function () {
    helper = can.Mustache._helpers.date.fn;
  });

  it('returns date only when boolean true is passed in', function () {
    instance = new Date(2015, 4, 3, 12, 34, 56);
    expect(helper(instance, true)).toEqual('05/03/2015');
  });

  it('returns datetime when stringy truthy value is passed in', function () {
    var timezone = moment(
      '2015-05-03T12:34:45Z').tz(moment.tz.guess()).format('A z');
    instance = new Date(2015, 4, 3, 12, 34, 56);

    expect(helper(instance, 'true')).toEqual('05/03/2015 12:34:56 '+ timezone);
  });

  it('returns datetime when stringy falsey value is passed in', function () {
    var timezone = moment(
      '2015-05-03T12:34:45Z').tz(moment.tz.guess()).format('A z');
    instance = new Date(2015, 4, 3, 12, 34, 56);

    expect(
      helper(instance, 'false')).toEqual('05/03/2015 12:34:56 '+ timezone);
  });

  it('returns datetime when false value is passed in', function () {
    var timezone = moment(
      '2015-05-03T12:34:45Z').tz(moment.tz.guess()).format('A z');
    instance = new Date(2015, 4, 3, 12, 34, 56);

    expect(
      helper(instance, false)).toEqual('05/03/2015 12:34:56 '+ timezone);
  });


  it('returns datetime when random values are passed in', function () {
    var timezone = moment(
      '2015-05-03T12:34:45Z').tz(moment.tz.guess()).format('A z');
    instance = new Date(2015, 4, 3, 12, 34, 56);

    expect(
      helper(instance, 'asdasd')).toEqual('05/03/2015 12:34:56 '+ timezone);
    expect(
      helper(instance, {a: 1})).toEqual('05/03/2015 12:34:56 '+ timezone);
    expect(
      helper(instance, '{a: 1}')).toEqual('05/03/2015 12:34:56 '+ timezone);
    expect(
      helper(instance, 123)).toEqual('05/03/2015 12:34:56 '+ timezone);
  });

});
