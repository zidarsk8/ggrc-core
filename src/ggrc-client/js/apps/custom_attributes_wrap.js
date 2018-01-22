/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {getCustomAttributeType} from '../plugins/utils/ca-utils';

export default can.Component.extend({
  tag: 'custom-attributes-wrap',
  template: '<content/>',
  scope: {
    define: {
      attributeValues: {
        get() {
          let result = [];

          can.each(this.attr('instance.custom_attribute_definitions'),
            (cad) => {
              let cav;
              let type = cad.attribute_type;
              can.each(this.attr('instance.custom_attribute_values'),
                (val) => {
                  val = val.isStub ? val : val.reify();
                  if (val.custom_attribute_id === cad.id) {
                    cav = val;
                  }
                });
              result.push({
                cav: cav,
                cad: {
                  id: cad.id,
                  attribute_type: cad.attribute_type,
                  mandatory: cad.mandatory,
                  title: cad.title,
                  label: cad.label,
                  placeholder: cad.placeholder,
                  helptext: cad.helptext,
                  multi_choice_options: cad.multi_choice_options,
                },
                type: getCustomAttributeType(type),
              });
            });
          return result;
        },
      },
    },
    instance: null,
    items: [],
    setItems: function (isReady) {
      let values = [];
      if (isReady) {
        values = this.attr('attributeValues').sort(function (a, b) {
          return a.cad.id - b.cad.id;
        });
        this.attr('items', values);
      }
    },
  },
  init: function () {
    if (this.scope.instance.class.is_custom_attributable) {
      this.scope.instance.setup_custom_attributes();
    }
    this.scope.setItems(true);
  },
  events: {
    '{scope.instance} readyForRender': function (sc, ev, isReady) {
      this.scope.setItems(isReady);
    },
  },
});
