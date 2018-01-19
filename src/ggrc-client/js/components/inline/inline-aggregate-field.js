/*
  Copyright (C) 2018 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './inline-aggregate-field.mustache';
import viewModelBase from '../aggregate-field-vm';

const viewModel = viewModelBase.extend({
  define: {
    aggregateValue: {
      type: 'string',
      get: function () {
        const items = this.attr('items');
        return items.join(', ');
      },
    },
  },
});

export default can.Component.extend({
  tag: 'inline-aggregate-field',
  template,
  viewModel,
  events: {
    '{viewModel} source': function () {
      this.viewModel.refreshItems();
    },
  },
});
