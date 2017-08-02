/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('can.mustache.helper.get_custom_attr_value', function () {
  'use strict';

  var helper;
  var fakeAttr;
  var fakeInstance;
  var fakeOptions;
  var fakeCustomAttrDefs;
  var origValue;
  var getHash;

  beforeAll(function () {
    helper = can.Mustache._helpers.get_custom_attr_value.fn;

    fakeCustomAttrDefs = [{
      definition_type: 'control',
      id: 3,
      attribute_type: '',
      title: 'Type'
    }];

    origValue = GGRC.custom_attr_defs;
    GGRC.custom_attr_defs = fakeCustomAttrDefs;

    getHash = function (attrValue) {
      var value = new can.Map({
        customAttrItem: {
          attribute_value: attrValue,
          custom_attribute_id: 3
        }
      });

      spyOn(value.customAttrItem, 'reify')
        .and.returnValue(value.customAttrItem);

      return value;
    };
  });

  afterAll(function () {
    GGRC.custom_attr_defs = origValue;
  });

  beforeEach(function () {
    fakeInstance = {};
    fakeAttr = {};
    fakeOptions = {};
    fakeInstance.class = {table_singular: 'control'};

    fakeAttr.attr_name = 'Type';
  });

  it('reify() is exec if instance is not an Assessment', function () {
    fakeOptions.hash = getHash();
    helper(fakeAttr, fakeInstance, fakeOptions);

    expect(fakeOptions.hash.customAttrItem.reify).toHaveBeenCalled();
  });

  it('return correct value if customAttrItem is undefined', function () {
    var value;
    fakeOptions.hash = false;
    fakeInstance.custom_attribute_values = [
      getHash('correctValue').customAttrItem
    ];
    value = helper(fakeAttr, fakeInstance, fakeOptions);

    expect(value).toEqual('correctValue');
  });

  it('return correct value if customAttrItem is not undefined', function () {
    var value;
    fakeOptions.hash = getHash('correctValue');
    value = helper(fakeAttr, fakeInstance, fakeOptions);

    expect(value).toEqual('correctValue');
  });

  it('fn() exec and return correct value (person type)', function () {
    fakeOptions = {
      hash: getHash(),
      contexts: {
        add: function () {
          return 'correctValue';
        }
      },
      fn: function (value) {
        return value;
      }
    };
    spyOn(fakeOptions, 'fn');
    fakeCustomAttrDefs[0].attribute_type = 'Map:';
    helper(fakeAttr, fakeInstance, fakeOptions);

    expect(fakeOptions.fn).toHaveBeenCalledWith('correctValue');
  });
});
