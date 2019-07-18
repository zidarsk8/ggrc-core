/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import canStache from 'can-stache';
import canMap from 'can-map';
import canComponent from 'can-component';
import '../dropdown/dropdown-component';
import '../numberbox/numberbox-component';
import template from './templates/modal-issue-tracker-fields.stache';

export default canComponent.extend({
  tag: 'modal-issue-tracker-fields',
  view: canStache(template),
  leakScope: true,
  viewModel: canMap.extend({
    instance: {},
    note: '',
    linkingNote: '',
    mandatoryTicketIdNote: '',
    isTicketIdMandatory: false,
    setTicketIdMandatory() {
      let instance = this.attr('instance');

      if (instance.constructor.unchangeableIssueTrackerIdStatuses) {
        this.attr('isTicketIdMandatory',
          instance.constructor.unchangeableIssueTrackerIdStatuses
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
