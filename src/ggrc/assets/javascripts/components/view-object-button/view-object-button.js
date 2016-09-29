/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can) {
  'use strict';

  GGRC.Components('viewObjectButton', {
    tag: 'view-object-button',
    template: can.view(
      GGRC.mustache_path +
      '/components/view-object-button/view-object-button.mustache'
    ),
    scope: {
      instance: null
    }
  });
})(window.can);
