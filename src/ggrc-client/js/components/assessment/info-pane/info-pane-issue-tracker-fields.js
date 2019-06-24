/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanComponent from 'can-component';
import '../../assessment/info-pane/confirm-edit-action';
import template from './templates/info-pane-issue-tracker-fields.stache';

export default CanComponent.extend({
  tag: 'info-pane-issue-tracker-fields',
  view: can.stache(template),
  leakScope: true,
  viewModel: can.Map.extend({
    define: {
      isTicketIdMandatory: {
        get() {
          let instance = this.attr('instance');
          return instance.class.unchangeableIssueTrackerIdStatuses
            .includes(instance.attr('status'));
        },
      },
    },
    instance: {},
  }),
});
