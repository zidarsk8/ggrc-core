/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can) {
  'use strict';

  /**
   * Simple wrapper component to load Related to Parent Object Audits
   */
  can.Component.extend({
    tag: 'related-audits',
    viewModel: {
      define: {
        parentInstance: {
          value: {}
        },
        // Load only Audits
        relatedTypes: {
          type: String,
          value: function () {
            return 'Audit';
          }
        }
      }
    }
  });
})(window.can);
