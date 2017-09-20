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
    var customAttrItem;
    var getValue;
    var formatValueMap = {
      Checkbox: function (item) {
        return ['No', 'Yes'][item.attribute_value];
      },
      Date: function (item) {
        return GGRC.Utils.formatDate(item.attribute_value, true);
      },
      'Map:Person': function (item) {
        return options.fn(options.contexts.add({
          object: item.attribute_object ? item.attribute_object.reify() : null
        }));
      }
    };

    attr = Mustache.resolve(attr);
    instance = Mustache.resolve(instance);
    customAttrItem = Mustache.resolve(customAttrItem);

    if (!(instance instanceof CMS.Models.Assessment)) {
      // reify all models with the exception of the Assessment,
      // because it has a different logic of work with the CA
      customAttrItem = customAttrItem.reify();

      // Getting a definition should be done with a def map for both
      // assessment and non assessment objects.
      definition = _.find(instance.custom_attribute_definitions, function(def){
        return def.id == customAttrItem.custom_attribute_id
      });
    } else {
      // In assessments we have custom attr def right in the CAV
      definition = customAttrItem.def
    }

    // Parent mustache helper should not loop through all and expect this
    // filter to work. It should only call this once with the correct CAV
    // see tree-item-custom-attribute.mustache - for every single value that
    // it needs to display, it loop through all values and then hopefully just
    // displays the single one that matches the column name
    // NOTE: The current implementation of the mustache file is also really bad
    // for performance!
    if (definition.title !== attr.attr_title) {
      return ''
    }

    if (formatValueMap[definition.attribute_type]) {
      value = formatValueMap[definition.attribute_type](customAttrItem);
    } else {
      value = customAttrItem.attribute_value;
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
