/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  'use strict';

  GGRC.Components('inlineEditControl', {
    tag: 'inline-edit-control',
    template: can.view(
      GGRC.mustache_path + '/components/inline/inline.mustache'
    ),
    viewModel: {
      editMode: false,
      withReadMore: false,
      isLoading: false,
      type: '@',
      value: '@',
      placeholder: '@',
      dropdownOptions: [],
      dropdownNoValue: false,
      isAllowEdit: true,
      context: {
        value: null
      },
      changeEditMode: function (editMode) {
        if (!editMode) {
          this.attr('editMode', false);
        }

        if (this.attr('isAllowEdit')) {
          this.attr('editMode', true);
        }
      },
      setPerson: function (scope, el, ev) {
        this.attr('context.value', ev.selectedItem.serialize());
      },
      unsetPerson: function (scope, el, ev) {
        ev.preventDefault();
        this.attr('context.value', undefined);
      },
      save: function () {
        var oldValue = this.attr('value');
        var value = this.attr('context.value');

        this.attr('editMode', false);
        // In case value is String and consists only of spaces - do nothing
        if (typeof value === 'string' && !value.trim()) {
          this.attr('context.value', '');
          value = null;
        }

        if (oldValue === value) {
          return;
        }

        this.attr('value', value);

        this.dispatch({
          type: 'inlineSave',
          value: value
        });
      },
      cancel: function () {
        var value = this.attr('value');
        this.attr('editMode', false);
        this.attr('context.value', value);
      },
      updateContext: function () {
        var value = this.attr('value');
        this.attr('context.value', value);
      },
      fieldValueChanged: function (args) {
        this.attr('context.value', args.value);
      }
    },
    events: {
      init: function () {
        this.viewModel.updateContext();
      },
      '{window} mousedown': function (el, ev) {
        var viewModel = this.viewModel;
        var editIcon = $(ev.target).hasClass('inline-edit-icon');
        var isInside = GGRC.Utils.events.isInnerClick(this.element, ev.target);
        var editMode = viewModel.attr('editMode');

        if (!isInside && editMode) {
          viewModel.cancel();
        }

        if (isInside && !editMode && editIcon) {
          viewModel.changeEditMode(true);
        }
      },
      '{viewModel} value': function () {
        // update value in the readonly mode
        if (!this.viewModel.attr('editMode')) {
          this.viewModel.updateContext();
        }
      }
    }
  });
})(window.can, window.can.$);
