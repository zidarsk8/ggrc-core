/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './collapsible-panel-header.stache';

/**
 * Collapsible Panel component to add collapsing behavior
 */
export default CanComponent.extend({
  tag: 'collapsible-panel-header',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    titleIcon: null,
    expanded: null,
    toggle: function () {
      this.attr('expanded', !this.attr('expanded'));
    },
  }),
});
