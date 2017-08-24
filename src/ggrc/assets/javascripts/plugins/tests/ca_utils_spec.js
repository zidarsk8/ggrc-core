/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

'use strict';

describe('GGRC utils isEmptyCustomAttribute() method', function () {
  var isEmptyCA;

  beforeAll(function () {
    isEmptyCA = GGRC.Utils.CustomAttributes.isEmptyCustomAttribute;
  });

  describe('check undefined value', function () {
    it('returns true for undefined', function () {
      var result = isEmptyCA(undefined);
      expect(result).toBe(true);
    });
  });

  describe('check Rich Text value', function () {
    it('returns true for empty div', function () {
      var result = isEmptyCA('<div></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns true for div with a line break', function () {
      var result = isEmptyCA('<div><br></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns true for div with a empty list', function () {
      var result = isEmptyCA('<div><ul><li></li></ul></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns true for div with a empty paragraph', function () {
      var result = isEmptyCA('<div><p></p></div>', 'Rich Text');
      expect(result).toBe(true);
    });

    it('returns false for div with the text', function () {
      var result = isEmptyCA('<div>Very important text!</div>', 'Rich Text');
      expect(result).toBe(false);
    });

    it('returns false for not empty list', function () {
      var result = isEmptyCA('<div><ul><li>One</li><li>Two</li></ul></div>',
        'Rich Text');
      expect(result).toBe(false);
    });
  });

  describe('check Checkbox value', function () {
    it('returns false for unchecked', function () {
      var result = isEmptyCA('0', 'Checkbox');
      expect(result).toBe(true);
    });

    it('returns true for checked', function () {
      var result = isEmptyCA('1', 'Checkbox');
      expect(result).toBe(false);
    });
  });

  describe('check Text value', function () {
    it('returns false for not empty', function () {
      var result = isEmptyCA('some text', 'Text');
      expect(result).toBe(false);
    });

    it('returns true for empty', function () {
      var result = isEmptyCA('', 'Text');
      expect(result).toBe(true);
    });
  });

  describe('check Map:Person type', function () {
    it('returns false for selected', function () {
      var result = isEmptyCA('Person', 'Map:Person');
      expect(result).toBe(false);
    });

    it('returns true for not selected', function () {
      var result = isEmptyCA('', 'Map:Person');
      expect(result).toBe(true);
    });

    it('returns true for not selected cav', function () {
      var result = isEmptyCA('', 'Map:Person', {attribute_object: null});
      expect(result).toBe(true);
    });

    it('returns false for selected cav', function () {
      var result = isEmptyCA('', 'Map:Person', {attribute_object: 'Person'});
      expect(result).toBe(false);
    });
  });

  describe('check Date type', function () {
    it('returns false for selected', function () {
      var result = isEmptyCA('01/01/2016', 'Date');
      expect(result).toBe(false);
    });

    it('returns true for not selected', function () {
      var result = isEmptyCA('', 'Date');
      expect(result).toBe(true);
    });
  });

  describe('check Dropdown type', function () {
    it('returns false for selected', function () {
      var result = isEmptyCA('value', 'Dropdown');
      expect(result).toBe(false);
    });

    it('returns true for not selected', function () {
      var result = isEmptyCA('', 'Dropdown');
      expect(result).toBe(true);
    });
  });

  describe('check invalid type', function () {
    it('returns false for invalid type', function () {
      var result = isEmptyCA('some value', 'Invalid');
      expect(result).toBe(false);
    });
  });

  describe('check validateField', function () {
    var validateField = GGRC.Utils.CustomAttributes.validateField;
    var CA_DD_REQUIRED_DEPS = GGRC.Utils.CustomAttributes.CA_DD_REQUIRED_DEPS;
    var inputField;
    var dropdownField;
    var checkboxField;

    beforeEach(function () {
      inputField = {
        attributeType: 'input',
        validationConfig: null,
        preconditions_failed: null,
        validation: {
          mandatory: false
        }
      };

      dropdownField = {
        attributeType: 'dropdown',
        validationConfig: {
          'nothing required': CA_DD_REQUIRED_DEPS.NONE,
          'comment required': CA_DD_REQUIRED_DEPS.COMMENT,
          'evidence required': CA_DD_REQUIRED_DEPS.EVIDENCE,
          'com+ev required': CA_DD_REQUIRED_DEPS.COMMENT_AND_EVIDENCE
        },
        preconditions_failed: [],
        validation: {
          mandatory: false
        }
      };

      checkboxField = {
        attributeType: 'checkbox',
        validationConfig: null,
        preconditions_failed: null,
        validation: {
          mandatory: false
        }
      };
    });

    it('should validate non-mandatory checkbox', function () {
      expect(validateField(checkboxField, null)).toEqual({
        validation: {
          show: false,
          valid: true,
          hasMissingInfo: false
        }
      });

      expect(validateField(checkboxField, '1')).toEqual({
        validation: {
          show: false,
          valid: true,
          hasMissingInfo: false
        }
      });
    });

    it('should validate mandatory checkbox', function () {
      checkboxField.validation.mandatory = true;
      expect(validateField(checkboxField, null)).toEqual({
        validation: {
          show: true,
          valid: false,
          hasMissingInfo: false
        }
      });
      expect(validateField(checkboxField, 0)).toEqual({
        validation: {
          show: true,
          valid: false,
          hasMissingInfo: false
        }
      });
      expect(validateField(checkboxField, 1)).toEqual({
        validation: {
          show: true,
          valid: true,
          hasMissingInfo: false
        }
      });

      expect(validateField(checkboxField, '1')).toEqual({
        validation: {
          show: true,
          valid: true,
          hasMissingInfo: false
        }
      });
    });

    it('should validate non-mandatory input', function () {
      expect(validateField(inputField, '')).toEqual({
        validation: {
          show: false,
          valid: true,
          hasMissingInfo: false
        }
      });

      expect(validateField(inputField, 'some input')).toEqual({
        validation: {
          show: false,
          valid: true,
          hasMissingInfo: false
        }
      });
    });

    it('should validate mandatory input', function () {
      inputField.validation.mandatory = true;

      expect(validateField(inputField, '')).toEqual({
        validation: {
          show: true,
          valid: false,
          hasMissingInfo: false
        }
      });

      expect(validateField(inputField, 'some input')).toEqual({
        validation: {
          show: true,
          valid: true,
          hasMissingInfo: false
        }
      });
    });

    it('should validate dropdown with not selected value', function () {
      // Nothing selected. i.e. None
      dropdownField.preconditions_failed = ['value'];

      expect(validateField(dropdownField, '')).toEqual({
        validation: {
          show: false,
          valid: false,
          hasMissingInfo: false
        },
        errorsMap: {
          comment: false,
          evidence: false
        }
      });
    });

    it('should validate dropdown with a plain value', function () {
      expect(validateField(dropdownField, 'nothing required')).toEqual({
        validation: {
          show: true,
          valid: true,
          hasMissingInfo: false
        },
        errorsMap: {
          comment: false,
          evidence: false
        }
      });
    });

    it('should validate dropdown with a comment required value and comment ' +
       'missing', function () {
      dropdownField.preconditions_failed = ['comment'];

      expect(validateField(dropdownField, 'comment required')).toEqual({
        validation: {
          show: true,
          valid: false,
          hasMissingInfo: true
        },
        errorsMap: {
          comment: true,
          evidence: false
        }
      });
    });

    it('should validate dropdown with a comment required value and comment ' +
       'present', function () {
      dropdownField.preconditions_failed = [];

      expect(validateField(dropdownField, 'comment required')).toEqual({
        validation: {
          show: true,
          valid: true,
          hasMissingInfo: false
        },
        errorsMap: {
          comment: false,
          evidence: false
        }
      });
    });

    it('should validate dropdown with an evidence required value and ' +
       'evidence missing', function () {
      dropdownField.preconditions_failed = ['evidence'];

      expect(validateField(dropdownField, 'evidence required')).toEqual({
        validation: {
          show: true,
          valid: false,
          hasMissingInfo: true
        },
        errorsMap: {
          comment: false,
          evidence: true
        }
      });
    });

    it('should validate dropdown with an evidence required value and ' +
       'evidence present', function () {
      dropdownField.preconditions_failed = [];

      expect(validateField(dropdownField, 'evidence required')).toEqual({
        validation: {
          show: true,
          valid: true,
          hasMissingInfo: false
        },
        errorsMap: {
          comment: false,
          evidence: false
        }
      });
    });

    it('should validate dropdown with both evidence and ' +
       'comment required values with both of them missing', function () {
      dropdownField.preconditions_failed = ['evidence', 'comment'];

      expect(validateField(dropdownField, 'com+ev required')).toEqual({
        validation: {
          show: true,
          valid: false,
          hasMissingInfo: true
        },
        errorsMap: {
          comment: true,
          evidence: true
        }
      });
    });

    it('should validate dropdown with both evidence and ' +
       'comment required values with evidence missing', function () {
      dropdownField.preconditions_failed = ['evidence'];

      expect(validateField(dropdownField, 'com+ev required')).toEqual({
        validation: {
          show: true,
          valid: false,
          hasMissingInfo: true
        },
        errorsMap: {
          comment: false,
          evidence: true
        }
      });
    });

    it('should validate dropdown with both evidence and ' +
       'comment required values with comment missing', function () {
      dropdownField.preconditions_failed = ['comment'];

      expect(validateField(dropdownField, 'com+ev required')).toEqual({
        validation: {
          show: true,
          valid: false,
          hasMissingInfo: true
        },
        errorsMap: {
          comment: true,
          evidence: false
        }
      });
    });

    it('should validate dropdown with both evidence and ' +
       'comment required values with both of present', function () {
      dropdownField.preconditions_failed = [];

      expect(validateField(dropdownField, 'com+ev required')).toEqual({
        validation: {
          show: true,
          valid: true,
          hasMissingInfo: false
        },
        errorsMap: {
          comment: false,
          evidence: false
        }
      });
    });
  });
});
