/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './multiselect-form-field-view.stache';

export default can.Component.extend({
  tag: 'multiselect-form-field-view',
  view: can.stache(template),
  leakScope: false,
  viewModel: can.Map.extend({
    value: null,
    disabled: false,
  }),
});
