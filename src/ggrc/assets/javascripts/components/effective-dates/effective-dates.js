/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, GGRC) {
  'use strict';

  GGRC.Components('effective-dates', {
    tag: 'effective-dates',
    template: can.view(
      GGRC.mustache_path +
      '/components/effective-dates/effective-dates.mustache'
    ),
    scope: {
      instance: null,
    }
  });
})(window.can, window.GGRC);
