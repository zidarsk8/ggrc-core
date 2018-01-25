/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('can.mustache.helper.get_default_attr_value', function () {
  'use strict';

  let helper;
  let instance;  // an object the helper retrieves an attribute value from

  beforeAll(function () {
    helper = can.Mustache._helpers.get_default_attr_value.fn;
  });

  beforeEach(function () {
    instance = new can.Map({});
  });

  it('returns an empty string if the attribute is missing', function () {
    let result = helper('does_not_exist', instance);
    expect(result).toEqual('');
  });

  it('returns an empty string if the attribute is not considered as "default"',
    function () {
      let result;
      instance.attr('is_not_default', true);
      result = helper('is_not_default', instance);
      expect(result).toEqual('');
    });

  describe('retrieving a "default" (non-date) attribute', function () {
    beforeEach(function () {
      instance.attr('status', 'Open');
    });

    it('returns a correct value through the .attr() method', function () {
      let result;
      spyOn(instance, 'attr').and.returnValue('In progress');

      result = helper('status', instance);

      expect(instance.attr).toHaveBeenCalledWith('status');
      expect(result).toEqual('In progress');
    });

    it('returns "true" string when boolean attr value is true', function () {
      let result;
      instance.attr('archived', true);
      result = helper('archived', instance);
      expect(result).toEqual('true');
    });

    it('returns "false" string when boolean attr value is false', function () {
      let result;
      instance.attr('archived', false);
      result = helper('archived', instance);
      expect(result).toEqual('false');
    });
  });

  describe('retrieving a date-like attribute', function () {
    beforeEach(function () {
      instance.attr('start_date', '1980-05-17');
    });

    it('returns a correctly formatted value through the .attr() method',
      function () {
        let result;
        spyOn(instance, 'attr').and.returnValue('2016-01-22');

        result = helper('start_date', instance);

        expect(instance.attr).toHaveBeenCalledWith('start_date');
        expect(result).toEqual('01/22/2016');
      }
    );
  });
});
