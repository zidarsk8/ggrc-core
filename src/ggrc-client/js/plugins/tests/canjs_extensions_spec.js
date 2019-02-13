/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('CanJS extensions', function () {
  describe('using camelCaseToUnderscore', function () {
    let method;

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
});
