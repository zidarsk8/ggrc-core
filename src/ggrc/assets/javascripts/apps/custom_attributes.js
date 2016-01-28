/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/

(function (can, $) {
  can.Component.extend({
    tag: 'custom-attributes',
    scope: {
      instance: null,
      // Make sure custom_attribute_definitions & custom_attribute_values
      // get loaded
      load: '@',
      loading: false
    },
    content: '<content/>',
    events: {
    },
    init: function () {
      var instance = this.scope.instance;
      var scope = this.scope;

      if (!instance.class.is_custom_attributable) {
        return;
      }
      if (this.scope.load) {
        scope.attr('loading', true);
        $.when(
          instance.load_custom_attribute_definitions(),
          instance.refresh_all('custom_attribute_values')
        ).always(function () {
          scope.attr('loading', false);
        });
      }
    },
    helpers: {
      with_value_for_id: function (id, options) {
        var ret;
        id = Mustache.resolve(id);
        can.each(this.instance.custom_attribute_values, function (value) {
          value = value.reify();
          if (value.custom_attribute_id === id) {
            ret = value.attribute_value;
          }
        });
        return options.fn(options.contexts.add({
          value: ret
        }));
      }
    }
  });
})(window.can, window.can.$);
