/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

describe('can.mustache.helper.model_info', function () {
  'use strict';

  var helper;
  var fakeModel;
  var fakeOptions;  // a fake "options" argument
  var origModel;  // the original model, if any, in the CMS.Models

  beforeAll(function () {
    helper = can.Mustache._helpers.model_info.fn;
  });

  beforeEach(function () {
    origModel = CMS.Models.ModelFoo;
    fakeModel = {};
    CMS.Models.ModelFoo = fakeModel;

    fakeOptions = {};
  });

  afterEach(function () {
    CMS.Models.ModelFoo = origModel;
  });

  it('returns the value of the correct model attribute', function () {
    var result;
    fakeModel.someAttribute = 'foo bar baz';
    result = helper('ModelFoo', 'someAttribute', fakeOptions);
    expect(result).toEqual('foo bar baz');
  });

  it('raises an error on missing arguments', function () {
    expect(function () {
      helper('ModelFoo', fakeOptions);
    }).toThrow(new Error('Invalid number of arguments (1), expected 2.'));
  });

  it('raises an error on too many arguments', function () {
    expect(function () {
      helper('ModelFoo', 'property1', 'property2', fakeOptions);
    }).toThrow(new Error('Invalid number of arguments (3), expected 2.'));
  });

  it('raises an error on an unknown model', function () {
    delete CMS.Models.ModelFoo;

    expect(function () {
      helper('ModelFoo', 'property', fakeOptions);
    }).toThrow(new Error('Model not found (ModelFoo).'));
  });
});
