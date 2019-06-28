/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import canStache from 'can-stache';
import canMap from 'can-map';
import CanComponent from 'can-component';
import template from './inner-nav-collapse.stache';

export default CanComponent.extend({
  tag: 'inner-nav-collapse',
  leakScope: false,
  view: canStache(template),
  viewModel: canMap.extend({
    title: null,
    expanded: true,
    toggle() {
      let expanded = this.attr('expanded');
      this.attr('expanded', !expanded);
    },
  }),
});
