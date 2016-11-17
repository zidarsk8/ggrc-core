/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, GGRC) {
  'use strict';

  GGRC.Components('mappingTypeSelector', {
    tag: 'mapping-type-selector',
    template: can.view(
      GGRC.mustache_path +
      '/components/mapping-controls/mapping-type-selector.mustache'
    ),
    scope: {
      disabled: false,
      readonly: false,
      types: [],
      selectedType: ''
    },
    events: {
      init: function () {
        // We might need to add some specific logic for disabled/enable DropDown items
      }
    }
  });
})(window.can, window.GGRC);
