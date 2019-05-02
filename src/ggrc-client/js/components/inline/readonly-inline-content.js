/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import '../form/fields/dropdown-form-field';
import '../person/person-data';
import template from './readonly-inline-content.stache';

export default can.Component.extend({
  tag: 'readonly-inline-content',
  view: can.stache(template),
  leakScope: true,
  viewModel: can.Map.extend({
    withReadMore: false,
    value: '',
    define: {
      items: {
        get() {
          let value = this.attr('value');
          if (value && typeof(value) === 'string') {
            return value.split(',')
              .map((item) => `<p><i class="fa fa-circle"></i>${item}</p>`)
              .join('');
          }
          return '';
        },
      },
    },
  }),
});
