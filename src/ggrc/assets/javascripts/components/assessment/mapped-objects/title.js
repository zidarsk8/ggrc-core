/*!
 Copyright (C) 2016 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var namespace = 'assessment';
  var cmpName = 'mapped-objects';
  var tpl = can.view(GGRC.mustache_path +
    '/components/' + namespace + '/' + cmpName + '/title.mustache');
  var tag = 'assessment-mapped-objects-title';
  /**
   * Assessment specific filtering mapped objects component
   */
  GGRC.Components('assessmentMappedObjectsTitle', {
    tag: tag,
    template: tpl,
    scope: {
      titleText: null,
      toggle: function () {
        this.attr('expanded', !this.attr('expanded'));
      }
    }
  });
})(window.can, window.GGRC);
