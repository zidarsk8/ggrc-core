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
      displayTab: {
        get() {
          let widget = this.attr('widget');
          let inForceShowList = this.attr('inForceShowList');

          return widget.attr('hasCount') &&
              widget.attr('count') ||
              widget.attr('uncountable') ||
              widget.attr('forceShow') ||
              this.attr('showAllTabs') ||
              inForceShowList;
        },
      },
      showCloseButton: {
        get() {
          return this.attr('widget.hasCount')
            && !this.attr('widget.count')
            && !this.attr('showAllTabs')
            && !this.attr('inForceShowList');
        },
      },
      inForceShowList: {
        get() {
          return _.includes(this.attr('forceShowList'),
            this.attr('widget.title'));
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
