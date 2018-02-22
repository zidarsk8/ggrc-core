/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {getCustomAttributeType} from '../plugins/utils/ca-utils';
const tag = 'custom-attributes-wrap';

export default can.Component.extend({
  tag,
  viewModel: {
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
    setItems(isReady) {
      let values = [];
      if (isReady) {
        values = this.attr('attributeValues')
          .sort((a, b) => a.cad.id - b.cad.id);
        this.attr('items', values);
      }
    },
  },
  init() {
    if (this.viewModel.instance.class.is_custom_attributable) {
      this.viewModel.instance.setup_custom_attributes();
    }
    this.viewModel.setItems(true);
  },
  events: {
    '{viewModel.instance} readyForRender'(sc, ev, isReady) {
      this.viewModel.setItems(isReady);
    },
  },
});
