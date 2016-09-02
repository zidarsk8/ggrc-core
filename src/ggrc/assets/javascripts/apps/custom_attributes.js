/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  GGRC.Components('customAttributes', {
    tag: 'custom-attributes',
    template: '<content/>',
    scope: {
      instance: null,
      items: [],
      setItems: function () {
        this.attr('items', this.getValues());
      },
      getValues: function () {
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
              type: GGRC.Utils.mapCAType(type)
            });
          }.bind(this));
        return result;
      }
    },
    init: function () {
      if (this.scope.instance.class.is_custom_attributable) {
        this.scope.instance.setup_custom_attributes();
      }
      this.scope.setItems();
    }
  });
})(window.can, window.GGRC);
