/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './templates/text-form-field.mustache';

const TEXT_FORM_FIELD_VM = {
  define: {
    inputValue: {
      set(newValue) {
        let _value = this.attr('_value');
        if (_value === newValue ||
          newValue.length && !can.trim(newValue).length) {
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
      set(newValue) {
        this.attr('_value', newValue);
      },
      get() {
        return this.attr('_value');
      },
    },
  },
  fieldId: null,
  placeholder: '',
  _value: '',
  valueChanged(newValue) {
    this.dispatch({
      type: 'valueChanged',
      fieldId: this.fieldId,
      value: newValue,
    });
  },
};

export default can.Component.extend({
  template,
  tag: 'text-form-field',
  viewModel: TEXT_FORM_FIELD_VM,
});

export {TEXT_FORM_FIELD_VM};
