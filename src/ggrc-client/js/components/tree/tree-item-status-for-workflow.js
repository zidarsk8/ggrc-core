/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './templates/tree-item-status-for-workflow.mustache';

const viewModel = can.Map.extend({
  define: {
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
});

export default can.Component({
  tag: 'tree-item-status-for-workflow',
  template,
  viewModel,
});
