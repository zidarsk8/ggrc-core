/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can) {
  'use strict';

  GGRC.Components('subTreeExpander', {
    tag: 'sub-tree-expander',
    template: '<content/>',
    viewModel: {
      expanded: null,
      disabled: false,
      onChangeState: null,
      onExpand: function () {
        this.attr('expanded', !this.attr('expanded'));
        this.onChangeState(this.attr('expanded'));
      }
    }
  });
})(window.can);
