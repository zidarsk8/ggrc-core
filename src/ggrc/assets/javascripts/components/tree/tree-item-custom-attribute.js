/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './templates/tree-item-custom-attribute.mustache';

var viewModel = can.Map.extend({
  instance: null,
  values: [],
  column: {}
});

var helpers = {
  /*
    Used to get the string value for custom attributes
  */
  get_custom_attr_value: function (attr, instance, customAttrItem, options) {
    var value = '';
    var definition;
    var formatValueMap = {
      Checkbox: function (item) {
        return ['No', 'Yes'][item.attribute_value];
      },
      Date: function (item) {
        return GGRC.Utils.formatDate(item.attribute_value, true);
      },
      'Map:Person': function (item) {
        return options.fn(options.contexts.add({
          object: item.attribute_object ? item.attribute_object.reify() : null,
        }));
      },
    };

    attr = Mustache.resolve(attr);
    instance = Mustache.resolve(instance);
    customAttrItem = Mustache.resolve(customAttrItem);

    can.each(GGRC.custom_attr_defs, function (item) {
      if (item.definition_type === instance.class.table_singular &&
        item.title === attr.attr_name) {
        definition = item;
      }
    });

    if (definition) {
      if (!(instance instanceof CMS.Models.Assessment)) {
        // reify all models with the exception of the Assessment,
        // because it has a different logic of work with the CA
        customAttrItem = customAttrItem.reify();
      }
      if (customAttrItem.custom_attribute_id === definition.id) {
        if (formatValueMap[definition.attribute_type]) {
          value =
            formatValueMap[definition.attribute_type](customAttrItem);
        } else {
          value = customAttrItem.attribute_value;
        }
      }
    }

    return value || '';
  }
};

GGRC.Components('treeItemCustomAttribute', {
  tag: 'tree-item-custom-attribute',
  template: template,
  viewModel: viewModel,
  helpers: helpers
});

export default helpers;
