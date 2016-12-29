/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  GGRC.Components('treeChildShow', {
    tag: 'tree-child-show',
    template: '<content/>',
    scope: {},
    events: {
      init: function (element, options) {
        this.scope.attr('controller', this);
        this.scope.attr('$rootEl', $(element));
      },
      'a click': function () {
        var sec_el = this.element.closest('section');
        var tree_view_el = sec_el.find('.cms_controllers_tree_view');
        var control = tree_view_el.control();
        var cur = control.options.attr('showMappedToAllParents');

        control.options.attr('showMappedToAllParents', !cur);
      }
    }
  });
})(window.can, window.can.$);
