/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../dropdown/dropdown';
import '../numberbox/numberbox';
import template from './templates/modal-issue-tracker-fields.mustache';
import {showTrackerNotification} from
  './temporary-issue-tracker-notification';

const tag = 'modal-issue-tracker-fields';

export default GGRC.Components('modalIssueTrackerFields', {
  tag: tag,
  template: template,
  viewModel: {
    instance: {},
    issueTrackerEnabled: false,
  },
  events: {
    inserted() {
      this.viewModel.attr('issueTrackerEnabled',
        this.viewModel.instance.issueTrackerEnabled());
    },
    '{viewModel.instance.issue_tracker} hotlist_id'() {
      if (this.viewModel.attr('issueTrackerEnabled') &&
        this.viewModel.instance.attr('type') === 'Assessment') {
        showTrackerNotification();
      }
    },
  },
});
