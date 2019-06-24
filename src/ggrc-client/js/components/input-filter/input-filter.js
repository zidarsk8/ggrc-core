/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './templates/input-filter.stache';

export default CanComponent.extend({
  tag: 'input-filter',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    value: '',
    excludeSymbols: '',
    placeholder: '',
    name: '',
    tabindex: 0,
    autofocus: false,
    exclude(value, symbols) {
      const regex = new RegExp(`[${symbols}]`, 'gi');

      return value.replace(regex, '');
    },
    cleanUpInput(el) {
      const excludeSymbols = this.attr('excludeSymbols');
      const originalValue = el.val();
      const result = this.exclude(originalValue, excludeSymbols);

      el.val(result);
    },
  }),
  events: {
    '.input-filter input'(el) {
      this.viewModel.cleanUpInput(el);
    },
  },
});
