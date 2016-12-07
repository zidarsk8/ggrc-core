/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  GGRC.Components('snapshotLoaderItem', {
    tag: 'snapshot-loader-item',
    template: can.view(
      GGRC.mustache_path +
      '/components/snapshot-loader/snapshot-loader-item.mustache'
    ),
    scope: {
      itemData: null,
      toggleIconCls: function () {
        return this.attr('showDetails') ? 'fa-caret-down' : 'fa-caret-right';
      },
      toggleDetails: function () {
        this.attr('showDetails', !this.attr('showDetails'));
      }
    },
    events: {}
  });
})(window.can, window.GGRC);
