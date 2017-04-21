/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can) {
  'use strict';

  /**
   * Simple wrapper component for related assessments table
   */
  can.Component.extend({
    tag: 'related-assessment-list',
    viewModel: {
      assessments: null,
      itemsLoading: function () {
        var items = this.attr('assessments');
        if (!items) {
          return false;
        }

        return _.any(items, function (item) {
          return item.attr('itemLoading');
        });
      }
    }
  });
})(window.can);
