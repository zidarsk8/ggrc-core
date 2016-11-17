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
      instance: null,
      define: {
        maximize: {
          type: 'boolean',
          'default': false
        }
      },
      maximizeObject: function (scope, el, ev) {
        var tree = el.closest('.cms_controllers_tree_view_node');
        var node = tree.control();
        ev.preventDefault();
        ev.stopPropagation();
        if (node) {
          node.select('max');
        }
      }
    }
  });
})(window.can);
