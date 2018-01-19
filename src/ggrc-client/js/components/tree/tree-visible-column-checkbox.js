/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './templates/tree-visible-column-checkbox.mustache';
const tag = 'tree-visible-column-checkbox';

export default can.Component.extend({
  tag,
  template,
  viewModel: {
    column: {},
    onChange(attr) {
      attr.attr('selected', !attr.attr('selected'));
    },
  },
});
