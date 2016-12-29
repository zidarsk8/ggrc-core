/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  can.Component.extend({
    tag: 'tree-type-selector',
    // <content> in a component template will be replaced with whatever is contained
    //  within the component tag.  Since the views for the original uses of these components
    //  were already created with content, we just used <content> instead of making
    //  new view template files.
    template: '<content/>',
    scope: {},
    events: {
      init: function (element, options) {
        this.scope.attr('controller', this);
        this.scope.attr('$rootEl', $(element));
      },

      'input.model-checkbox click': function (el, ev) {
        ev.stopPropagation();
      },

      '.dropdown-menu-form click': function (el, ev) {
        ev.stopPropagation();
      },

      update_check_boxes: function (el, ev) {
        // change checkboxes based on the model_type
        // get the closest tree_view controller, change the options to reload the checkboxes.
        var i;
        var select_el = this.element.find('.object-type-selector');
        var model_name = select_el.val();
        var sec_el = select_el.closest('section');
        var tree_view_el = sec_el.find('.cms_controllers_tree_view');
        var control = tree_view_el.control();
        var display_list = GGRC.tree_view.sub_tree_for[model_name].display_list;
        var select_model_list = GGRC.tree_view.sub_tree_for[model_name].model_list;
        var obj;

        // set up display status for UI
        for (i = 0; i < select_model_list.length; i++) {
          obj = select_model_list[i];
          obj.display_status = display_list.indexOf(obj.model_name) !== -1;
        }
        control.options.attr('selected_child_tree_model_list', select_model_list);
      },

      'select.object-type-selector change': 'update_check_boxes',

      'a.select-all click': function (el, ev) {
        var $check = this.element.find('.model-checkbox');

        $check.prop('checked', true);
      },

      'a.select-none click': function (el, ev) {
        var $check = this.element.find('.model-checkbox');

        $check.prop('checked', false);
      },

      '.set-display-object-list,.close-dropdown click': function (el, ev) {
        this.scope.$rootEl.removeClass('open');
        this.scope.$rootEl.parents('.dropdown-menu')
          .parent().removeClass('open');
      }
    }
  });
})(window.can, window.can.$);
