/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can) {
  'use strict';

  GGRC.Components('addObjectButton', {
    tag: 'add-object-button',
    template: can.view(
      GGRC.mustache_path +
      '/components/add-object-button/add-object-button.mustache'
    ),
    scope: {
      instance: null,
      linkclass: '@',
      content: '@',
      title: '@',
      singular: '@',
      plural: '@'
    }
  });
})(window.can);
