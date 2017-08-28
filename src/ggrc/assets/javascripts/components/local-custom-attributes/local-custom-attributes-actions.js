/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can) {
  'use strict';

  GGRC.Components('localCustomAttributesActions', {
    tag: 'local-custom-attributes-actions',
    template: can.view(
      GGRC.mustache_path + '/components/local-custom-attributes/' +
        'local-custom-attributes-actions.mustache'
    ),
    viewModel: {
      formEditMode: false,
      edit: function () {
        this.attr('formEditMode', true);
      }
    }
  });
})(window.can);
