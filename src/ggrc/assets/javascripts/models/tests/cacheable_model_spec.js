/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('CMS.Models.Cacheable', function () {
  'use strict';

  describe('setup_custom_attributes() method', function () {
    var instance;

    function customAttrFactory(id, type, title) {
      return new can.Map({
        id: id,
        attribute_type: type,
        title: title
      });
    }

    beforeEach(function () {
      instance = new can.Model.Cacheable({
        custom_attribute_definitions: new can.List(),
        custom_attribute_values: new can.List()
      });
    });

    it('sorts custom attribute definitions by ascending IDs', function () {
      var expectedIdOrder;
      var definitions = new can.List([
        customAttrFactory(3, 'Text', 'CA three'),
        customAttrFactory(5, 'Text', 'CA five'),
        customAttrFactory(2, 'Text', 'CA two'),
        customAttrFactory(4, 'Text', 'CA four'),
        customAttrFactory(1, 'Text', 'CA one')
      ]);
      instance.custom_attribute_definitions.replace(definitions);

      instance.setup_custom_attributes();

      expectedIdOrder = _.map(instance.custom_attribute_definitions, 'id');
      expect(expectedIdOrder).toEqual([1, 2, 3, 4, 5]);
    });

    it('skips sorting if no custom attribute definitions', function () {
      var actualOrder;
      instance.attr('custom_attribute_definitions', undefined);
      instance.setup_custom_attributes();
      actualOrder = _.map(instance.custom_attribute_definitions, 'id');
      expect(actualOrder).toEqual([]);
    });
  });
});
