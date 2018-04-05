/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import tracker from '../../tracker';
import {
  getPageType,
} from '../../plugins/utils/current-page-utils';
import template from './cycle-task-actions.mustache';
import WorkflowHelpers from '../workflow/workflow-helpers';

(function (can, GGRC) {
  'use strict';

  let viewModel = can.Map.extend({
    define: {
      cycle: {
        get: function () {
          return this.attr('instance').cycle;
        },
      },
      workflow: {
        get: function () {
          return this.attr('instance.cycle.workflow');
        },
      },
      cssClasses: {
        type: String,
        get: function () {
          let classes = [];

          if (this.attr('disabled')) {
            classes.push('disabled');
          }

          return classes.join(' ');
        },
      },
      isShowActionButtons: {
        get: function () {
          let pageType = getPageType();
          let allowChangeState = this.attr('instance.allow_change_state');

          if (pageType === 'Workflow') {
            return this.attr('cycle').reify().attr('is_current');
          }

          return allowChangeState;
        },
      },
    },
    instance: null,
    disabled: false,
    oldValues: [],
    changeStatus: function (ctx, el, ev) {
      let status = el.data('value');
      let instance = this.attr('instance');
      let oldValue = {
        status: instance.attr('status'),
      };

      ev.stopPropagation();
      this.attr('oldValues').unshift(oldValue);

      this.setStatus(status);
    },
    undo: function (ctx, el, ev) {
      let newValue = this.attr('oldValues').shift();
      ev.stopPropagation();

      this.setStatus(newValue.status);
    },
    async setStatus(status) {
      const instance = this.attr('instance');
      const stopFn = tracker.start(
        instance.type,
        tracker.USER_JOURNEY_KEYS.LOADING,
        tracker.USER_ACTIONS.CYCLE_TASK.CHANGE_STATUS);
      this.attr('disabled', true);
      await WorkflowHelpers.updateStatus(instance, status);
      this.attr('disabled', false);
      stopFn();
    },
  });

  /**
   *
   */
  GGRC.Components('cycleTaskActions', {
    tag: 'cycle-task-actions',
    template: template,
    viewModel: viewModel,
    events: {
      inserted: function () {
      },
    },
  });
})(window.can, window.GGRC);
