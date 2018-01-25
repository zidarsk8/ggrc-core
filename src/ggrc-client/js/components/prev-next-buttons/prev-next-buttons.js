/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './prev-next-buttons.mustache';

(function (can, GGRC, CMS) {
  'use strict';

  GGRC.Components('prevNextButtons', {
    tag: 'prev-next-buttons',
    template: template,
    viewModel: {
      define: {
        currentIndex: {
          type: 'number'
        },
        totalCount: {
          type: 'number'
        },
        hasNext: {
          get: function () {
            let current = this.attr('currentIndex');
            let total = this.attr('totalCount');
            return current < total - 1;
          }
        },
        hasPrev: {
          get: function () {
            let current = this.attr('currentIndex');
            return current > 0;
          }
        }
      },
      setNext: function () {
        let current = this.attr('currentIndex');
        let hasNext = this.attr('hasNext');

        if (hasNext) {
          this.attr('currentIndex', current + 1);
        }
      },
      setPrev: function () {
        let current = this.attr('currentIndex');
        let hasPrev = this.attr('hasPrev');

        if (hasPrev) {
          this.attr('currentIndex', current - 1);
        }
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
