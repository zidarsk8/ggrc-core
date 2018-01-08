/*!
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';
  /*
   * Child component that tracks checkbox changes
   *
   * Values that we pass in:
   * - reusable - If reusable checkbox should be visible
   * - method - Which method from parent (reuse-objects) component should be used
   *            for makining relationship
   * - list - List on which set if item should be reused
   */
  can.Component.extend({
    tag: 'reusable-object',
    template: '<content></content>',
    scope: {
      list: null
    },
    helpers: {
      isDisabled: function (instance, options) {
        var isMapped = GGRC.Utils.is_mapped(
          this.attr('baseInstance'), instance, this.attr('mapping'));

        if (isMapped) {
          return options.fn(options.contexts);
        }
        return options.inverse(options.context);
      }
    }
  });
})(window.can, window.GGRC);
