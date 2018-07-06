/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import '../person/person-data';
import '../review-link/review-link';

import template from './approval-link.mustache';

export default can.Component.extend({
  tag: 'approval-link',
  template,
  viewModel: {
    instance: null,
  },
});
