/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  'use strict';

  GGRC.Components('inlineDropdown', {
    tag: 'inline-dropdown',
    template: can.view(
      GGRC.mustache_path +
      '/components/inline_edit/dropdown.mustache'
    ),
    scope: {
    },
    events: {
    }
  });
})(window.can, window.can.$);
