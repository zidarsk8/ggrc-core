/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/tree/tree-item-status-for-workflow.mustache');
  /**
   *
   */
  GGRC.Components('treeItemStatusForWorkflow', {
    tag: 'tree-item-status-for-workflow',
    template: template,
    viewModel: {
      define: {
        isOverdue: {
          type: 'boolean',
          get: function () {
            var resolvedDate = this.attr('instance.end_date');
            var hashDueDate = this.attr('instance.next_due_date');
            var nextDueDate = moment(hashDueDate || resolvedDate);
            var endDate = moment(resolvedDate);
            var date = moment.min(nextDueDate, endDate);
            var today = moment().startOf('day');
            var startOfDate = moment(date).startOf('day');
            var isBefore = date && today.diff(startOfDate, 'days') >= 0;
            var status = this.attr('instance.status');
            return (status !== 'Verified' && isBefore);
          }
        },
        statusCSSClass: {
          type: 'string',
          get: function () {
            var cssClass = [];
            cssClass.push(this.attr('instance.status') ?
            'status-' + this.attr('instance.status').toLowerCase() : '');
            cssClass.push(this.attr('instance.overdue') ?
            'status-' + this.attr('instance.overdue').toLowerCase() : '');
            cssClass.push(this.attr('isOverdue') ?
              'status-overdue' : '');
            return cssClass.join(' ');
          }
        }
      },
      instance: {}
    }
  });
})(window.can, window.GGRC);
