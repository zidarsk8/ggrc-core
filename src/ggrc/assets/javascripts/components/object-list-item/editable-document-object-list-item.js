/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/object-list-item/editable-document-object-list-item.mustache');
  var tag = 'editable-document-object-list-item';

  GGRC.Components('editableDocumentObjectListItem', {
    tag: tag,
    template: tpl,
    viewModel: {
      document: null
    }
  });
})(window.can, window.GGRC);
