/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanComponent from 'can-component';
import template from './custom-attributes-actions.stache';

export default CanComponent.extend({
  tag: 'custom-attributes-actions',
  view: can.stache(template),
  leakScope: true,
  viewModel: can.Map.extend({
    instance: null,
    formEditMode: false,
    disabled: false,
    edit: function () {
      this.attr('formEditMode', true);
    },
  }),
});
