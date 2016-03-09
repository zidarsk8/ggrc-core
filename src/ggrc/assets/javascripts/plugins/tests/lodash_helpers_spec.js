/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: ivan@reciprocitylabs.com
  Maintained By: ivan@reciprocitylabs.com
*/

describe('_.splitTrim() method', function () {
  'use strict';

  describe('Given an string with dots and dot splitter', function () {
    var input = 'a. b. c. d. a. b . . b';
    var splitter = '.';

    it('return split without spaces', function () {
      var result = _.splitTrim(input, splitter);
      expect(result).toEqual(['a', 'b', 'c', 'd', 'a', 'b', '', 'b']);
    });

    it('return unique values without spaces', function () {
      var result = _.splitTrim(input, splitter, {
        unique: true
      });
      expect(result).toEqual(['a', 'b', 'c', 'd', '']);
    });

    it('return compact values without spaces', function () {
      var result = _.splitTrim(input, splitter, {
        compact: true
      });
      expect(result).toEqual(['a', 'b', 'c', 'd', 'a', 'b', 'b']);
    });

    it('return compact and uniquee values without spaces', function () {
      var result = _.splitTrim(input, splitter, {
        unique: true,
        compact: true
      });
      expect(result).toEqual(['a', 'b', 'c', 'd']);
    });
  });

  describe('Given an string with commas given default splitter', function () {
    var input = 'a,b,c , d ,c,a  b, , , f';

    it('return values without spaces', function () {
      var result = _.splitTrim(input);
      expect(result).toEqual(['a', 'b', 'c', 'd', 'c', 'a  b', '', '', 'f']);
    });

    it('return unique split values without spaces', function () {
      var result = _.splitTrim(input, {
        unique: true
      });
      expect(result).toEqual(['a', 'b', 'c', 'd', 'a  b', '', 'f']);
    });

    it('return compact split values without spaces', function () {
      var result = _.splitTrim(input, {
        compact: true
      });
      expect(result).toEqual(['a', 'b', 'c', 'd', 'c', 'a  b', 'f']);
    });

    it('return unique and compact split values without spaces', function () {
      var result = _.splitTrim(input, {
        compact: true,
        unique: true
      });
      expect(result).toEqual(['a', 'b', 'c', 'd', 'a  b', 'f']);
    });
  });

  describe('Given no value', function () {
    it('returns empty array', function () {
      var result = _.splitTrim(undefined);
      expect(result).toEqual([]);
    });
  });
});
