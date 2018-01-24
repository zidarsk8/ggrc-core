/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('can.mustache.helper.ca_validation_error', function () {
  'use strict';

  var helper;
  var fakeOptions;

  beforeAll(function () {
    helper = can.Mustache._helpers.ca_validation_error.fn;
  });

  beforeEach(function () {
    fakeOptions = {
      fn: jasmine.createSpy('options.fn'),
      inverse: jasmine.createSpy('options.inverse'),
      contexts: {
        add: jasmine.createSpy('contexts.add')
      }
    };
  });

  it('renders the "truthy" block if there are validation errors for the ' +
    'custom attribute',
    function () {
      var validationErrors = {
        'custom_attributes.4': ['invalid value']
      };
      helper(validationErrors, 4, fakeOptions);
      expect(fakeOptions.fn).toHaveBeenCalled();
    }
  );

  it('adds the errors list to the scope if there are validation errors for ' +
    'the custom attribute',
    function () {
      var validationErrors = {
        'custom_attributes.1': ['invalid  date format'],
        'custom_attributes.4': ['value is too short', 'not a number']
      };
      helper(validationErrors, 4, fakeOptions);
      expect(fakeOptions.contexts.add).toHaveBeenCalledWith(
        {errors: ['value is too short', 'not a number']}
      );
    }
  );

  it('renders the "falsy" block if there are no validation errors for the ' +
    'custom attribute',
    function () {
      var validationErrors = {
        'custom_attributes.4': ['invalid value']
      };
      helper(validationErrors, 8, fakeOptions);
      expect(fakeOptions.inverse).toHaveBeenCalled();
    }
  );
});
