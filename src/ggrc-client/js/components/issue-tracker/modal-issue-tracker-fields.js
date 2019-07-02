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
import {
  checkIssueTrackerTicketId,
} from '../../plugins/utils/issue-tracker-utils';
import {validateAttr} from '../../plugins/utils/validation-utils';
import {getAjaxErrorInfo} from '../../plugins/utils/errors-utils';
import {notifier} from '../../plugins/utils/notifiers-utils';

const state = {
  NOT_SELECTED: 0,
  GENERATE_NEW: 1,
  LINK_TO_EXISTING: 2,
  LINKED: 3,
};

export default canComponent.extend({
  tag: 'modal-issue-tracker-fields',
  view: canStache(template),
  leakScope: true,
  viewModel: canMap.extend({
    define: {
      displayFields: {
        get() {
          return this.attr('instance.issue_tracker.enabled') &&
            this.attr('currentState') !== state.NOT_SELECTED;
        },
      },
      ticketIdErrorMessage: {
        get() {
          const instance = this.attr('instance');
          const validationError =
            validateAttr(instance, 'issue_tracker.issue_id');
          if (validationError) {
            return validationError;
          }

          const hasTicketIdError = this.attr('isTicketIdChecked') &&
            !this.attr('isTicketIdCheckSuccessful');

          return hasTicketIdError ? this.attr('ticketIdCheckMessage') : '';
        },
      },
      isTicketIdDisabled: {
        get() {
          return this.attr('isTicketIdChecking') ||
            !this.attr('instance.issue_tracker.issue_id');
        },
      },
    },
    instance: {},
    note: '',
    mandatoryTicketIdNote: '',
    isTicketIdMandatory: false,
    state,
    currentState: state.NOT_SELECTED,
    isTicketIdChecking: false,
    isTicketIdChecked: false,
    isTicketIdCheckSuccessful: false,
    ticketIdCheckMessage: '',
    generateNewTicket() {
      if (this.attr('currentState') === state.GENERATE_NEW) {
        return;
      }

      this.attr('currentState', state.GENERATE_NEW);
      this.setValidationFlags({linking: false, initialized: true});

      this.attr('instance').setDefaultHotlistAndComponent();
      this.attr('instance.issue_tracker.issue_id', null);
    },
    linkToExistingTicket() {
      if (this.attr('currentState') === state.LINK_TO_EXISTING) {
        return;
      }

      this.attr('currentState', state.LINK_TO_EXISTING);
      this.setValidationFlags({linking: true, initialized: true});

      this.attr('instance.issue_tracker').attr({
        issue_id: null,
        hotlist_id: null,
        component_id: null,
      });
    },
    setTicketIdMandatory() {
      let instance = this.attr('instance');

      if (instance.constructor.unchangeableIssueTrackerIdStatuses) {
        this.attr('isTicketIdMandatory',
          instance.constructor.unchangeableIssueTrackerIdStatuses
            .includes(instance.attr('status')));
      }
    },
    setValidationFlags({initialized, linking}) {
      this.attr('instance.issue_tracker').attr({
        is_linking: linking,
        _initialized: initialized,
      });
    },
    statusChanged() {
      this.setTicketIdMandatory();

      if (this.attr('currentState') === state.GENERATE_NEW &&
        this.attr('isTicketIdMandatory')) {
        this.linkToExistingTicket();
      }
    },
    checkTicketId() {
      const instance = this.attr('instance');
      if (this.attr('isTicketIdDisabled')) {
        return;
      }

      this.attr('isTicketIdChecking', true);
      this.attr('isTicketIdChecked', false);
      this.attr('isTicketIdCheckSuccessful', false);

      return checkIssueTrackerTicketId(instance.issue_tracker.issue_id)
        .then((data) => {
          const type = data.type;
          const id = data.id;
          if (type && id && type === instance.type && id === instance.id) {
            // ignore 'valid' field, because ticket has already
            // linked to current instance

            this.attr('isTicketIdCheckSuccessful', true);
            this.attr('ticketIdCheckMessage', '');
          } else {
            this.attr('isTicketIdCheckSuccessful', data.valid);
            this.attr('ticketIdCheckMessage', data.msg);
          }

          this.attr('isTicketIdChecked', true);
        })
        .fail((xhr) => {
          this.resetTicketIdCheckState();
          notifier('error', getAjaxErrorInfo(xhr).details);
        })
        .always(() => {
          this.attr('isTicketIdChecking', false);
        });
    },
    resetTicketIdCheckState() {
      this.attr('isTicketIdCheckSuccessful', false);
      this.attr('ticketIdCheckMessage', '');
      this.attr('isTicketIdChecked', false);
    },
  }),
  events: {
    inserted() {
      let vm = this.viewModel;

      vm.setTicketIdMandatory();
      if (vm.attr('instance').issueCreated()) {
        vm.attr('currentState', state.LINKED);
        vm.setValidationFlags({initialized: true, linking: false});
        return;
      }

      vm.setValidationFlags({initialized: false, linking: false});
    },
    '{viewModel.instance} status'() {
      this.viewModel.statusChanged();
    },
    removed() {
      let instance = this.viewModel.attr('instance');
      if (instance) {
        instance.removeAttr('issue_tracker.is_linking');
        instance.removeAttr('issue_tracker._initialized');
      }
    },
    '{viewModel.instance.issue_tracker} issue_id'() {
      this.viewModel.resetTicketIdCheckState();
    },
  },
});
