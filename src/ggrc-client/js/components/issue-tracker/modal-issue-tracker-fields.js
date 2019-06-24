/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import '../dropdown/dropdown-component';
import '../numberbox/numberbox-component';
import template from './templates/modal-issue-tracker-fields.stache';

export default CanComponent.extend({
  tag: 'modal-issue-tracker-fields',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    instance: {},
    note: '',
    linkingNote: '',
    mandatoryTicketIdNote: '',
    setIssueTitle: false,
    allowToChangeId: false,
    isTicketIdMandatory: false,
    setTicketIdMandatory() {
      let instance = this.attr('instance');

      if (instance.class.unchangeableIssueTrackerIdStatuses) {
        this.attr('isTicketIdMandatory',
          instance.class.unchangeableIssueTrackerIdStatuses
            .includes(instance.attr('status')));
      }
    },
  }),
  events: {
    inserted() {
      this.viewModel.setTicketIdMandatory();
    },
    '{viewModel.instance} status'() {
      this.viewModel.setTicketIdMandatory();
    },
  },
});
