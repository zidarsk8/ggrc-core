/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

'use strict';

import { isEmptyCustomAttribute as isEmptyCA } from '../../plugins/utils/ca-utils';

describe('GGRC utils isEmptyCustomAttribute() method', function () {

  describe('check undefined value', function () {
    it('returns true for undefined', function () {
      let result = isEmptyCA(undefined);
      expect(result).toBe(true);
    });
  });

  describe('check Rich Text value', function () {
    it('returns true for empty div', function () {
      let result = isEmptyCA('<div></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns true for div with a line break', function () {
      let result = isEmptyCA('<div><br></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns true for div with a empty list', function () {
      let result = isEmptyCA('<div><ul><li></li></ul></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns true for div with a empty paragraph', function () {
      let result = isEmptyCA('<div><p></p></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns false for div with the text', function () {
      let result = isEmptyCA('<div>Very important text!</div>', 'Rich Text');
      expect(result).toBe(false);
    });

    it('returns false for not empty list', function () {
      let result = isEmptyCA('<div><ul><li>One</li><li>Two</li></ul></div>',
        'Rich Text');
      expect(result).toBe(false);
    });
  });

  describe('check Checkbox value', function () {
    it('returns false for unchecked', function () {
      let result = isEmptyCA('0', 'Checkbox');
      expect(result).toBe(true);
    });

    it('returns true for checked', function () {
      let result = isEmptyCA('1', 'Checkbox');
      expect(result).toBe(false);
    });
  });

  describe('check Text value', function () {
    it('returns false for not empty', function () {
      let result = isEmptyCA('some text', 'Text');
      expect(result).toBe(false);
    });

    it('returns true for empty', function () {
      let result = isEmptyCA('', 'Text');
      expect(result).toBe(true);
    });
  });

  describe('check Map:Person type', function () {
    it('returns false for selected', function () {
      let result = isEmptyCA('Person', 'Map:Person');
      expect(result).toBe(false);
    });

    it('returns true for not selected', function () {
      let result = isEmptyCA('', 'Map:Person');
      expect(result).toBe(true);
    });

    it('returns true for not selected cav', function () {
      let result = isEmptyCA('', 'Map:Person', {attribute_object: null});
      expect(result).toBe(true);
    });

    it('returns false for selected cav', function () {
      let result = isEmptyCA('', 'Map:Person', {attribute_object: 'Person'});
      expect(result).toBe(false);
    });
  });

  describe('check Date type', function () {
    it('returns false for selected', function () {
      let result = isEmptyCA('01/01/2016', 'Date');
      expect(result).toBe(false);
    });

    it('returns true for not selected', function () {
      let result = isEmptyCA('', 'Date');
      expect(result).toBe(true);
    });
  });

  describe('check Dropdown type', function () {
    it('returns false for selected', function () {
      let result = isEmptyCA('value', 'Dropdown');
      expect(result).toBe(false);
    });

    it('returns true for not selected', function () {
      let result = isEmptyCA('', 'Dropdown');
      expect(result).toBe(true);
    });
  });

  describe('check invalid type', function () {
    it('returns false for invalid type', function () {
      let result = isEmptyCA('some value', 'Invalid');
      expect(result).toBe(false);
    });
  });
});
