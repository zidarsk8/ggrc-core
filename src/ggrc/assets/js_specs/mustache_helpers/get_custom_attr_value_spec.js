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
    },
    {
      definition_type: 'control',
      title: 'CheckBox',
      attribute_type: 'checkbox',
      id: 4
    }];

    origValue = GGRC.custom_attr_defs;
    GGRC.custom_attr_defs = fakeCustomAttrDefs;

    getHash = function (attrValue, attrId, attrType) {
      var value = new can.Map({
        customAttrItem: {
          attribute_value: attrValue,
          custom_attribute_id: attrId || 3,
          attributeType: attrType
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

  it('return "No" if customAttrItem is undefined', function () {
    var value;
    fakeOptions.hash = false;
    fakeInstance.custom_attribute_values = [
      getHash('correctValue', undefined, 'checkbox').customAttrItem
    ];
    value = helper(fakeAttr, fakeInstance, fakeOptions);

    expect(value).toEqual('No');
  });

  it('return an empty string if customAttrItem is undefined', function () {
    var value;
    fakeOptions.hash = getHash();
    value = helper(fakeAttr, fakeInstance, fakeOptions);

    expect(value).toEqual('');
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

  it('returns "on" for CA of type checkbox with value "1"',
    function () {
      var attr = {
        attr_name: 'CheckBox'
      };
      var value;
      fakeOptions = {
        hash: getHash('1', 4, 'checkbox')
      };

      value = helper(attr, fakeInstance, fakeOptions);

      expect(value).toEqual('Yes');
    });

  it('returns "off" for CA of type checkbox with value "0"',
    function () {
      var attr = {
        attr_name: 'CheckBox'
      };
      var value;
      fakeOptions = {
        hash: getHash('0', 4, 'checkbox')
      };

      value = helper(attr, fakeInstance, fakeOptions);

      expect(value).toEqual('No');
    });

  it('returns "" for CA of type checkbox with value ""',
    function () {
      var attr = {
        attr_name: 'CheckBox'
      };
      var value;
      fakeOptions = {
        hash: getHash('', 4, 'checkbox')
      };

      value = helper(attr, fakeInstance, fakeOptions);

      expect(value).toEqual('No');
    });
});
