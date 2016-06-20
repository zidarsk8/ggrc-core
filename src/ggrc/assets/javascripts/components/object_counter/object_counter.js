/*!
 Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: urban@reciprocitylabs.com
 Maintained By: urban@reciprocitylabs.com
 */

(function (can, $) {
  'use strict';

  /**
   *  Component for object counting. This component relies on backend to
   *  provide specified counter in GGRC.page_object.counts.
   *
   *  @param {string} counter - Counter returned by backend in
   *    GGRC.page_object.counts.
   */
  GGRC.Components('ObjectCounter', {
    tag: 'object-counter',
    template: can.view(GGRC.mustache_path +
      '/components/object_counter/object_counter.mustache'),
    scope: {
      counter: '@',
      count: null,
      updateCount: function () {
        var counter = this.attr('counter');
        if (_.isUndefined(GGRC.counters[counter])) {
          throw new Error('Specified counter doesn\'t exist.');
        }
        this.attr('count', parseInt(GGRC.counters[counter], 10));
    },
    events: {
      inserted: function () {
        this.scope.updateCount();
      }
    }
  });
})(window.can, window.can.$);
