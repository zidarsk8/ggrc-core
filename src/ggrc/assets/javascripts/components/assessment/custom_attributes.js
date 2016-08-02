/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, can, GGRC) {
  'use strict';

  var fieldsTypeMap = {
    Text: 'input',
    'Rich Text': 'text',
    'Map:Person': 'person',
    Date: 'date',
    Input: 'input',
    Checkbox: 'checkbox',
    Dropdown: 'dropdown'
  };

  function getTypeFromCompounded(type) {
    type = can.Mustache.resolve(type);
    return fieldsTypeMap[type];
  }

  function isEmpty(value, type) {
    if (type === 'checkbox') {
      return !(value === '1');
    }
    return !value;
  }

  GGRC.Components('assessmentCustomAttributes', {
    tag: 'assessment-custom-attributes',
    scope: {
      instance: null,
      needConfirm: false,
      load: '@',
      loading: false,
      refreshAttributes: function () {
        this.attr('loading', true);
        can.$
          .when(
            this.instance.load_custom_attribute_definitions(),
            this.instance.refresh_all('custom_attribute_values')
              .then(function (values) {
                var rq = new window.RefreshQueue();
                _.each(values, function (value) {
                  if (value.attribute_object) {
                    rq.enqueue(value.attribute_object);
                  }
                });
                return rq.trigger();
              })
              .then(function () {
                this.instance.setup_custom_attributes();
              }.bind(this)))
          .always(function () {
            this.attr('loading', false);
          }.bind(this));
      }
    },
    content: '<content/>',
    init: function () {
      var scope = this.scope;
      var status = scope.instance.status;

      if (!scope.instance.class.is_custom_attributable) {
        return;
      }

      scope.attr('needConfirm',
        status === 'Completed' || status === 'Verified');

      if (scope.load) {
        scope.refreshAttributes();
      }
    },

    helpers: {
      mapFieldsType: function (type) {
        return getTypeFromCompounded(type);
      },
      mapValuesById: function (id, options) {
        var instance = this.instance;
        var invalidFields = instance.attr().invalidCustomAttributes || [];
        var mappedData = {
          value: null,
          valueId: null,
          validation: {
            mandatory: options.scope.attr('mandatory'),
            empty: true,
            valid: true
          }
        };

        id = can.Mustache.resolve(id);

        can.each(instance.custom_attribute_values, function (value) {
          value = value.reify();

          if (value.custom_attribute_id === id) {
            mappedData.valueId = value.id;
            mappedData.value = value.attribute_object ?
              value.attribute_object.reify() : value.attribute_value;
            mappedData.validation = {
              mandatory: options.scope.attr('mandatory'),
              empty: isEmpty(mappedData.value,
                getTypeFromCompounded(options.scope.attr('attribute_type'))),
              valid: invalidFields.every(function (x) {
                return x !== id;
              })
            };
          }
        });
        return options.fn(options.scope.add(mappedData));
      }
    }
  });
})(window._, window.can, window.GGRC);
