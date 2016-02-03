/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

describe('can.mustache.helper.get_default_attr_value', function () {
  'use strict';

  var helper;
  var instance;  // an object the helper retrieves an attribute value from

  beforeAll(function () {
    helper = can.Mustache._helpers.get_default_attr_value.fn;
  });

  beforeEach(function () {
    instance = new can.Map({});
  });

  it('returns an empty string if the attribute is missing', function () {
    var result = helper('does_not_exist', instance);
    expect(result).toEqual('');
  });

  it('returns an empty string if the attribute has a falsy value',
    function () {
      var result;
      instance.attr('foo', false);
      result = helper('foo', instance);
      expect(result).toEqual('');
    }
  );

  describe('retrieving a "default" (non-date) attribute', function () {
    beforeEach(function () {
      instance.attr('status', 'Open');
    });

    it('returns a correct value through the .attr() method', function () {
      var result;
      spyOn(instance, 'attr').and.returnValue('In progress');

      result = helper('status', instance);

      expect(instance.attr).toHaveBeenCalledWith('status');
      expect(result).toEqual('In progress');
    });
  });

  describe('retrieving a date-like attribute', function () {
    beforeEach(function () {
      instance.attr('start_date', '1980-05-17');
    });

    it('returns a correctly formatted value through the .attr() method',
      function () {
        var result;
        spyOn(instance, 'attr').and.returnValue('2016-01-22');

        result = helper('start_date', instance);

        expect(instance.attr).toHaveBeenCalledWith('start_date');
        expect(result).toEqual('01/22/2016');
      }
    );
  });
});
