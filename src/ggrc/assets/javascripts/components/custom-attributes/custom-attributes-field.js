/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC) {
  'use strict';

  GGRC.Components('localCustomAttributesField', {
    tag: 'custom-attributes-field',
    template: can.view(
      GGRC.mustache_path + '/components/custom-attributes/' +
        'custom-attributes-field.mustache'
    ),
    viewModel: {
      define: {
        disabled: {
          type: 'htmlbool'
        }
      },
      type: null,
      value: null,
      fieldId: null,
      placeholder: '',
      options: [],
      fieldValueChanged: function (e, scope) {
        this.dispatch({
          type: 'valueChanged',
          fieldId: e.fieldId,
          value: e.value,
          field: scope
        });
      }
    }
  });
})(window.can, window.GGRC);
