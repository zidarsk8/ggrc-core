/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import '../sort-component/sort-component';
import template from './templates/tree-view.stache';

let viewModel = CanMap.extend({
  define: {
    notResult: {
      type: Boolean,
      get: function () {
        return !this.attr('loading') && !this.attr('items').length;
      },
    },
  },
  items: [],
  parentInstance: null,
  model: null,
  selectedColumns: [],
  mandatory: [],
  disableConfiguration: null,
  loading: false,
  limitDepthTree: 0,
  depthFilter: '',
});

export default CanComponent.extend({
  tag: 'tree-view',
  view: can.stache(template),
  leakScope: true,
  viewModel,
});
