/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: ivan@reciprocitylabs.com
  Maintained By: ivan@reciprocitylabs.com
*/

describe('CanJS extensions', function () {
  'use strict';

  describe('using camelCaseToDashCase', function () {
    var method;

    beforeEach(function () {
      method = can.camelCaseToDashCase;
    });

    it('should return dash case from camel case', function () {
      expect(method('helloWorld')).toBe('hello-world');
      expect(method('helloWorldHiThere')).toBe('hello-world-hi-there');
      expect(method('MyNumber4AndNumber5')).toBe('my-number4and-number5');
    });
    it('should return same value for one word', function () {
      expect(method('hello')).toBe('hello');
      expect(method('Hello')).toBe('hello');
    });
    it('should return same value for dash case', function () {
      expect(method('hello-world')).toBe('hello-world');
      expect(method('hello-world-hi-there')).toBe('hello-world-hi-there');
    });
    it('should return emptry string in case of non string', function () {
      expect(method(42)).toBe('');
      expect(method({a: 1})).toBe('');
    });
  });
});
