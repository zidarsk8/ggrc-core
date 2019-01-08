/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
import template from './inner-nav-item.stache';

export default can.Component.extend({
  tag: 'inner-nav-item',
  template,
  viewModel: {
    define: {
      showCloseButton: {
        get() {
          return this.attr('widget.hasCount')
            && !this.attr('widget.count')
            && !this.attr('showAllTabs')
            && this.attr('forceShowList')
              .indexOf(this.attr('widget.title')) === -1;
        },
      },
      isActive: {
        get() {
          return this.attr('widget') === this.attr('activeWidget');
        },
      },
    },
    widget: null,
    showTitle: true,
    activeWidget: null,
    showAllTabs: false,
    forceShowList: [],
    closeTab() {
      this.dispatch({
        type: 'close',
        widget: this.attr('widget'),
      });

      // prevent click propagation
      return false;
    },
  },
});
