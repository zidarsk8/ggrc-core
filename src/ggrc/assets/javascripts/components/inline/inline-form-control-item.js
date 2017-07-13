/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can) {
  'use strict';

  GGRC.Components('inlineFormControlItem', {
    tag: 'inline-form-control-item',
    viewModel: {
      instance: {},
      isLoading: false,
      editMode: false,
      isAllowEdit: false,
      propName: '@',
      type: '@',
      value: '',
      dropdownOptions: [],
      dropdownClass: '@',
      dropdownNoValue: false,
      save: function (args) {
        var value = args.value;

        this.dispatch({
          type: 'inlineFormItemSave',
          propName: this.attr('propName'),
          value: value
        });
      }
    }
  });
})(window.can);
