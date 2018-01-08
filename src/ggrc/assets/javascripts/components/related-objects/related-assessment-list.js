/*!
 Copyright (C) 2018 Google Inc.
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
      define: {
        itemsLoading: {
          get: function () {
            // due to 'assessments' will be updated via
            // replace method, 'assessments.length' adds
            // subscription on 'add' and 'remove' events
            if (!this.attr('assessments.length')) {
              return false;
            }

            return _.any(this.attr('assessments'), function (item) {
              return item.attr('itemLoading');
            });
          }
        }
      },
      assessments: null
    }
  });
})(window.can);
