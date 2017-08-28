/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC, $) {
  'use strict';

  GGRC.Components('localCustomAttributes', {
    tag: 'local-custom-attributes',
    template: can.view(
      GGRC.mustache_path +
      '/components/local-custom-attributes/local-custom-attributes.mustache'
    ),
    viewModel: {
      fields: [],
      editMode: false,
      fieldValueChanged: function (e, field) {
        this.dispatch({
          type: 'valueChanged',
          fieldId: e.fieldId,
          value: e.value,
          field: field
        });
      }
    }
  });
})(window.can, window.GGRC, window.jQuery);
