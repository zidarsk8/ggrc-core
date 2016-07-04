/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  'use strict';

  GGRC.Components('sortBySortIndex', {
    tag: 'sort-by-sort-index',
    scope: {
      sorted: null,
      mapping: null,
      next_sort_index: null
    },

    init: function () {
      var mapping = this.scope.attr('mapping');
      var sort = function () {
        var arr = _.toArray(mapping);
        var last;
        var lastIndex;
        arr.sort(function (a, b) {
          a = a.instance.sort_index;
          b = b.instance.sort_index;
          if (a === b) {
            return 0;
          }
          return GGRC.Math.string_less_than(a, b) ? -1 : 1;
        });
        this.scope.attr('sorted', arr);
        last = arr[arr.length - 1];
        lastIndex = (last !== -Infinity) ? last.instance.sort_index : '0';
        this.scope.attr('next_sort_index',
            GGRC.Math.string_half(
                GGRC.Math.string_add(
                    Number.MAX_SAFE_INTEGER.toString(), lastIndex
                )
            )
        );
      }.bind(this);
      sort();
      mapping.bind('change', sort);
    },

    events: {
      ' sortupdate': function (el, ev, ui) {
        var mapping = this.scope.attr('mapping');
        var instanceIndex = _.indexBy(_.pluck(mapping, 'instance'), 'id');

        var instances = _.map(ui.item.parent().children('li'), function (el) {
          return instanceIndex[$(el).data('object-id')];
        });

        var targetIndex = _.findIndex(instances, {
          id: ui.item.data('object-id')
        });

        var nexts = []; // index for constant time next element lookup
        var dirty = []; // instances to be saved
        instances[targetIndex].attr('sort_index', null);
        nexts[instances.length] = Number.MAX_SAFE_INTEGER.toString();
        _.eachRight(instances, function (instance, index) {
          nexts[index] = instance.sort_index || nexts[index + 1];
        });

        // in most cases this will only update sort_index for targetIndex
        // but will also correctly resolve missing or duplicate sort_index-es
        _.each(instances, function (instance, index) {
          var prev;
          var next;
          if (instance.sort_index &&
              instance.sort_index !== nexts[index + 1]) {
            return;
          }
          prev = (instances[index - 1] || {sort_index: '0'}).sort_index;
          next = nexts[index + 1];
          instance.attr('sort_index', GGRC.Math.string_half(
                GGRC.Math.string_add(prev, next)
          ));
          dirty.push(instance);
        });

        _.each(dirty, function (instance) {
          var index = instance.sort_index;
          return instance.refresh().then(function (instance) {
            instance.attr('sort_index', index);
            instance.save();
          });
        });
      }
    }
  });
})(window.can, window.can.$);
