/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, can, GGRC) {
  'use strict';

  GGRC.Components('customAttributesObjectValueMapper', {
    tag: 'ca-object-value-mapper',
    template: '<content></content>',
    scope: {
      input: {
        value: null,
        type: null,
        options: [],
        placeholder: 'Please enter the value...'
      },
      value: null,
      valueObj: null,
      type: null,
      def: null,
      initInput: function () {
        this.attr('input', {
          options: this.getOptions(),
          value: this.getValue(),
          type: this.getType(),
          title: this.getTitle()
        });
      },
      getOptions: function () {
        var options = this.attr('def.multi_choice_options');
        return options && _.isString(options) ? options.split(',') : [];
      },
      getTitle: function () {
        return this.attr('def.title');
      },
      getType: function () {
        var type = this.attr('type');
        return type;
      },
      getValue: function () {
        var type = this.attr('type');
        var value = this.attr('value');
        var valueObj = this.attr('valueObj');

        if (type === 'checkbox') {
          return value === '1';
        }

        if (type === 'input') {
          if (!value) {
            return null;
          }
          return value.trim();
        }

        if (type === 'person') {
          if (valueObj) {
            return valueObj;
          }
          return null;
        }

        if (type === 'dropdown') {
          if (_.isNull(value) || _.isUndefined(value)) {
            return '';
          }
        }
        return value;
      },
      setValue: function (value) {
        var type = this.attr('type');
        value = this.formatValueByType(value, type);
        this.attr('value', value);
      },
      formatValueByType: function (value, type) {
        if (type === 'checkbox') {
          return value ? 1 : 0;
        }

        if (type === 'person') {
          if (value && value instanceof can.Map) {
            value = value.serialize();
            return 'Person:' + value.id;
          }
          return 'Person:None';
        }
        return value || null;
      }
    },

    events: {
      init: function () {
        this.scope.initInput();
      },
      '{scope.input} value': function (scope, ev, val) {
        this.scope.setValue(val);
      }
    }
  });
})(window._, window.can, window.GGRC);
