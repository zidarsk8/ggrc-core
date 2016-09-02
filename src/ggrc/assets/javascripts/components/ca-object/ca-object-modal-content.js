/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/ca-object/ca-object-modal-content.mustache');

  GGRC.Components('customAttributeObjectModalContent', {
    tag: 'ca-object-modal-content',
    template: tpl,
    scope: {
      content: {
        title: null,
        value: null,
        type: null
      },
      caIds: null
    },
    helpers: {
      renderFieldValue: function (value) {
        value = value();
        return value || '<span class="empty-message">None</span>';
      }
    }
  });
})(window.can, window.GGRC);
