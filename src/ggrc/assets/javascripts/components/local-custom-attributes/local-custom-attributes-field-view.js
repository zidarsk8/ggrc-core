/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC) {
  'use strict';

  GGRC.Components('localCustomAttributesFieldView', {
    tag: 'local-custom-attributes-field-view',
    template: can.view(
      GGRC.mustache_path + '/components/local-custom-attributes/' +
        'local-custom-attributes-field-view.mustache'
    ),
    viewModel: {
      type: null,
      value: null
    }
  });
})(window.can, window.GGRC);
