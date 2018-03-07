/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './templates/tree-item-status-for-workflow.mustache';

(function (can, GGRC) {
  'use strict';

  /**
   *
   */
  GGRC.Components('treeItemStatusForWorkflow', {
    tag: 'tree-item-status-for-workflow',
    template: template,
    viewModel: {
      define: {
        statusTitle: {
          type: 'string',
          get() {
            return this.attr('instance.status');
          },
        },
        statusCSSClass: {
          type: 'string',
          get() {
            const status = this.attr('instance.status');
            let result = '';

            if (status) {
              const postfix = status
                .replace(/[\s\t]+/g, '')
                .toLowerCase();
              result = `state-${postfix}`;
            }

            return result;
          },
        },
      },
      instance: {},
    },
  });
})(window.can, window.GGRC);
