/*!
 Copyright (C) 2017 Google Inc.
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
    viewModel: {
      activeModel: null,
      modelsList: [],
      selectedChildModels: [],
      onChildModelsChange: null
    },
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

      updateCheckBoxes: function (el, ev) {
        // change checkboxes based on the model_type
        // get the closest tree_view controller, change the options to reload the checkboxes.
        var i;
        var selectEl = this.element.find('.object-type-selector');
        var modelName = selectEl.val();
        var displayList;
        var selectModelList;
        var obj;

        if (!modelName) {
          modelName = this.viewModel.activeModel;
          selectEl.val(modelName);
        } else {
          this.viewModel.attr('activeModel', modelName);
        }

        displayList = GGRC.tree_view.sub_tree_for[modelName].display_list;
        selectModelList = GGRC.tree_view.sub_tree_for[modelName].model_list;

        // set up display status for UI
        for (i = 0; i < selectModelList.length; i++) {
          obj = selectModelList[i];
          obj.display_status = displayList.indexOf(obj.model_name) !== -1;
        }
        this.viewModel.attr('selectedChildModels', selectModelList.slice(0));
      },

      'select.object-type-selector change': 'updateCheckBoxes',

      '.tview-type-toggle click': 'updateCheckBoxes',

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
      },

      '.set-display-object-list click': function (ev) {
        var modelName = this.viewModel.activeModel;
        var $check = this.element.find('.model-checkbox');
        var $selected = $check.filter(':checked');
        var selectedItems = [];

        // save the list
        $selected.each(function (index) {
          selectedItems.push(this.value);
        });

        this.viewModel.onChildModelsChange(modelName, selectedItems);
      }
    }
  });
})(window.can, window.can.$);
