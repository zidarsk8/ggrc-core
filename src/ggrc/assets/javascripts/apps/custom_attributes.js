/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  'use strict';

  GGRC.Components('customAttributes', {
    tag: 'custom-attributes',
    scope: {
      instance: null,
      getValues: function () {
        var types = {
          Checkbox: 'checkbox',
          'Rich Text': 'text',
          Dropdown: 'dropdown',
          Date: 'date',
          Text: 'input',
          'Map:Person': 'person'
        };
        var result = [];

        can.each(this.attr('instance.custom_attribute_definitions'),
          function (cad) {
            var cav;
            var type = cad.attribute_type;
            can.each(this.attr('instance.custom_attribute_values'),
              function (val) {
                val = val.isStub ? val : val.reify();
                if (val.custom_attribute_id === cad.id) {
                  cav = val;
                }
              });
            result.push({
              cav: cav,
              cad: cad,
              type: types[type] ? types[type] : types.text
            });
          }.bind(this));
        return result;
      }
    },
    init: function () {
      if (this.scope.instance.class.is_custom_attributable) {
        this.scope.instance.setup_custom_attributes();
      }
    },
    events: {
    }
  });
})(window.can, window.can.$);
