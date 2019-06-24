/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanComponent from 'can-component';
import {
  getPageType,
} from '../../plugins/utils/current-page-utils';

export default CanComponent.extend({
  tag: 'sub-tree-expander',
  leakScope: true,
  viewModel: can.Map.extend({
    define: {
      contextName: {
        type: String,
        get: function () {
          return getPageType();
        },
      },
    },
    expandNotDirectly: function () {
      this.dispatch('expandNotDirectly');
    },
    expanded: null,
    disabled: false,
    onChangeState: null,
    onExpand: function () {
      this.attr('expanded', !this.attr('expanded'));
      this.onChangeState(this.attr('expanded'));
    },
  }),
});
