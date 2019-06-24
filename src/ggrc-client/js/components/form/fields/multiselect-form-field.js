/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './multiselect-form-field.stache';

export default CanComponent.extend({
  tag: 'multiselect-form-field',
  view: can.stache(template),
  leakScope: false,
  viewModel: CanMap.extend({
    define: {
      inputValue: {
        set(newValue) {
          this.attr('_value', newValue);
          this.valueChanged(newValue);
        },
        get() {
          return this.attr('_value');
        },
      },
      value: {
        set(newValue) {
          this.attr('_value', newValue);
        },
        get() {
          return this.attr('_value');
        },
      },
      options: {
        set(newValue) {
          this.attr('_options', newValue);
        },
        get() {
          const selected = this.attr('_value').split(',');
          return _.map(this.attr('_options'), (item) => {
            return {value: item, checked: selected.includes(item)};
          });
        },
      },
    },
    _value: '',
    _options: [],
    fieldId: null,
    isInlineMode: false,
    valueChanged(newValue) {
      this.dispatch({
        type: 'valueChanged',
        fieldId: this.fieldId,
        value: newValue.selected.map((item) => item.attr('value')).join(','),
      });
    },
  }),
});
