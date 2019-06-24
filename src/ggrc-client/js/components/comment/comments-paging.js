/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './comments-paging.stache';
import '../spinner-component/spinner-component';

export default CanComponent.extend({
  tag: 'comments-paging',
  view: can.stache(template),
  leakScope: false,
  viewModel: CanMap.extend({
    define: {
      showButton: {
        get() {
          return this.attr('total') > this.attr('pageSize') &&
            !this.attr('isLoading');
        },
      },
      canShowMore: {
        get() {
          return this.attr('comments.length') < this.attr('total');
        },
      },
      canHide: {
        get() {
          return this.attr('comments.length') > this.attr('pageSize');
        },
      },
      remain: {
        get() {
          let pageSize = this.attr('pageSize');
          let count = this.attr('total') - this.attr('comments.length');
          return count > pageSize ? pageSize : count;
        },
      },
    },
    comments: [],
    pageSize: 10,
    total: 0,
    isLoading: false,
    showMore() {
      this.dispatch({
        type: 'showMore',
      });
    },
    showLess() {
      this.dispatch({
        type: 'showLess',
      });
    },
  }),
});
