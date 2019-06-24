/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanComponent from 'can-component';
import template from './templates/info-issue-tracker-fields.stache';

export default CanComponent.extend({
  tag: 'info-issue-tracker-fields',
  view: can.stache(template),
  leakScope: true,
  viewModel: can.Map.extend({
    instance: {},
    showTitle: false,
    note: '',
    linkingNote: '',
    snowId: false,
  }),
});
