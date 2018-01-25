/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {
  getPageType,
} from '../../plugins/utils/current-page-utils';
import template from './cycle-task-actions.mustache';

(function (can, GGRC) {
  'use strict';

  let viewModel = can.Map.extend({
    define: {
      cycle: {
        get: function () {
          return this.attr('instance').cycle;
        }
      },
      workflow: {
        get: function () {
          return this.attr('instance.cycle.workflow');
        }
      },
      cssClasses: {
        type: String,
        get: function () {
          let classes = [];

          if (this.attr('disabled')) {
            classes.push('disabled');
          }

          return classes.join(' ');
        }
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
        status: instance.attr('status')
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
    setStatus: function (status) {
      let instance = this.attr('instance');

      this.attr('disabled', true);
      instance.refresh().then(function (refreshed) {
        refreshed.attr('status', status);

        return refreshed.save();
      }).then(function () {
        this.attr('disabled', false);
      }.bind(this));
    }
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
      }
    }
  });
})(window.can, window.GGRC);
