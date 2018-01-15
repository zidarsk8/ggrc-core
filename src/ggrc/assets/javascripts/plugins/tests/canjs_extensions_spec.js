/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
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
    it('should return empty string in case of non string', function () {
      expect(method(42)).toBe('');
      expect(method({a: 1})).toBe('');
    });
  });

  describe('using camelCaseToUnderscore', function () {
    var method;

    beforeEach(function () {
      method = can.camelCaseToUnderscore;
    });

    it('should return snake case from camel case', function () {
      expect(method('helloWorld')).toBe('hello_world');
      expect(method('helloWorldHiThere')).toBe('hello_world_hi_there');
      expect(method('MyNumber4AndNumber5')).toBe('my_number_4_and_number_5');
    });
    it('should return same value for one word', function () {
      expect(method('hello')).toBe('hello');
      expect(method('Hello')).toBe('hello');
    });
    it('should return same value for snake case', function () {
      expect(method('hello_world')).toBe('hello_world');
      expect(method('hello_world_hi_there')).toBe('hello_world_hi_there');
    });
    it('should throw a type error in case of non string', function () {
      expect(function () {
        method(42);
      }).toThrow(new TypeError('Invalid type, string required.'));
      expect(function () {
        method({a: 1});
      }).toThrow(new TypeError('Invalid type, string required.'));
    });
  });

  describe('using spaceCamelCase', function () {
    var method;

    beforeEach(function () {
      method = can.spaceCamelCase;
    });

    it('should return camel case from space case', function () {
      expect(method('hello_world')).toBe('Hello World');
      expect(method('hello_world_hi_there')).toBe('Hello World Hi There');
      expect(method('my_number_4_and_number_5')).toBe(
        'My Number 4 And Number 5');
    });
    it('should return same value for one word', function () {
      expect(method('hello')).toBe('Hello');
      expect(method('Hello')).toBe('Hello');
    });
    it('should return properly capitalized for camelCase input', function () {
      expect(method('helloWorld')).toBe('Hello World');
      expect(method('helloWorldHiThere')).toBe('Hello World Hi There');
    });
    it('should throw a type error in case of non string', function () {
      expect(function () {
        method(42);
      }).toThrow(new TypeError('Invalid type, string required.'));
      expect(function () {
        method({a: 1});
      }).toThrow(new TypeError('Invalid type, string required.'));
    });
  });
});
