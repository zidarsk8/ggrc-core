/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import tracker from '../../tracker';
import '../spinner/spinner';
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
    async changeStatus(ctx, el, ev) {
      let status = el.data('value');
      let instance = this.attr('instance');
      let oldValue = {
        status: instance.attr('status'),
      };

      ev.stopPropagation();
      const result = await this.setStatus(status);
      if (result) {
        this.attr('oldValues').unshift(oldValue);
      }
    },
    async undo(ctx, el, ev) {
      ev.stopPropagation();
      let previousValue = this.attr('oldValues.0');
      const result = await this.setStatus(previousValue.status);
      if (result) {
        this.attr('oldValues').shift();
      }
    },
    async setStatus(status) {
      const instance = this.attr('instance');
      const stopFn = tracker.start(
        instance.type,
        tracker.USER_JOURNEY_KEYS.LOADING,
        tracker.USER_ACTIONS.CYCLE_TASK.CHANGE_STATUS
      );
      this.attr('disabled', true);
      try {
        await WorkflowHelpers.updateStatus(instance, status);
        return true;
      } catch (e) {
        GGRC.Errors.notifier(
          'error',
          "Task state wasn't updated due to server error. Please try again."
        );
        return false;
      } finally {
        this.attr('disabled', false);
        stopFn();
      }
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
