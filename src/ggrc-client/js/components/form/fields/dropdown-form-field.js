/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../../dropdown/dropdown';
import template from './dropdown-form-field.mustache';

(function (can, GGRC) {
  'use strict';

  GGRC.Components('dropdownFormField', {
    tag: 'dropdown-form-field',
    template: template,
    viewModel: {
      define: {
        isNoneSelected: {
          get: function () {
            return this.attr('value') === null &&
              this.attr('disabled');
          },
        },
        inputValue: {
          set: function (newValue) {
            let oldValue = this.attr('_value');

            if (newValue === oldValue) {
              return;
            }

            this.attr('_value', newValue);
            this.valueChanged(newValue);
          },
          get() {
            return this.attr('_value');
          },
        },
        value: {
          set: function (newValue) {
            this.attr('_value', newValue);
          },
          get() {
            return this.attr('_value');
          },
        },
        fieldId: {
          type: 'number',
        },
      },
      _value: '',
      options: [],
      isGroupedDropdown: false,
      dropdownOptionsGroups: {},
      noValue: true,
      valueChanged: function (newValue) {
        this.dispatch({
          type: 'valueChanged',
          fieldId: this.attr('fieldId'),
          value: newValue,
        });
      },
    },
  });
})(window.can, window.GGRC);
