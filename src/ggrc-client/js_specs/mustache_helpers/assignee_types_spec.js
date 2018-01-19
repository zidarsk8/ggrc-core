/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('can.mustache.helper.assignee_types', function () {
  'use strict';

  let helper;

  beforeAll(function () {
    helper = can.Mustache._helpers.assignee_types.fn;
  });

  describe('expected assignee type with a capital letter in brackets,' +
    'when the input: ', function () {
    it('type in lower case', function () {
      expect(helper('foo')).toEqual('(Foo)');
    });

    it('type in upper case', function () {
      expect(helper('BAR')).toEqual('(Bar)');
    });

    it('type\'s letters in different cases', function () {
      expect(helper('bAz')).toEqual('(Baz)');
    });
  });

  describe('expected empty string ', function () {
    it('if input empty string', function () {
      expect(helper('')).toEqual('');
    });

    it('if input undefined', function () {
      expect(helper(undefined)).toEqual('');
    });

    it('if input null', function () {
      expect(helper(null)).toEqual('');
    });
  });

  describe('expected error for incorrect input types:', function () {
    it('number', function () {
      expect(function () {
        helper(123);
      }).toThrow();
    });

    it('array', function () {
      expect(function () {
        helper([1, 2, 3]);
      }).toThrow();
    });
  });
});
