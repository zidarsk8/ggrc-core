/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/search-toolbar/search-toolbar.mustache');
  var tag = 'search-toolbar';
  /**
   * Search Toolbar component
   */
  GGRC.Components('searchToolbar', {
    tag: tag,
    template: tpl,
    scope: {
    },
    events: {
    }
  });
})(window.can, window.GGRC);
