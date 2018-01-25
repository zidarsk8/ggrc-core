/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  'use strict';

  GGRC.Components('tasksSortList', {
    tag: 'tasks-sort-list',
    scope: {
      sorted: null,
      mapping: null,
      next_sort_index: null
    },

    init: function () {
      let mapping = this.scope.attr('mapping');
      this.sort(mapping);
      mapping.bind('change', _.bind(this.sort, this, mapping));
    },

    /**
     * Sort a list of tasks and update the next sort index.
     *
     * @param {can.List} mapping - a mapping representing a list of Tasks
     *   mapped to the "parent" object
     */
    sort: function (mapping) {
      let arr = _.toArray(mapping);
      let last;
      let lastIndex;

      arr.sort(this.compareTasks.bind(this));
      this.scope.attr('sorted', arr);

      last = arr[arr.length - 1];
      lastIndex = (last !== -Infinity && last) ?
          last.instance.sort_index :
          '0';
      this.scope.attr('next_sort_index',
          GGRC.Math.string_half(
              GGRC.Math.string_add(
                  Number.MAX_SAFE_INTEGER.toString(), lastIndex
              )
          )
      );
    },

    /**
     * Compare two Task definitions for sorting purposes.
     *
     * @param {CMS.Models.TaskGroupTask} a - the first Task to compare
     * @param {CMS.Models.TaskGroupTask} b - the second Task to compare
     *
     * @return {Number} - a number less than 0 if "a" should come first,
     *   greater than 0 if "b" should come first, or exactly zero if "a"
     *   and "b" are considered equal to each other.
     */
    compareTasks: function (a, b) {
      let ad = this.getTaskDate(a.instance, 'start');
      let bd = this.getTaskDate(b.instance, 'start');
      let result = ad - bd;

      if (!result) {  // if same start dates
        ad = this.getTaskDate(a.instance, 'end');
        bd = this.getTaskDate(b.instance, 'end');
        result = ad - bd;
      }
      return result;
    },

    /**
     * Get the date on which the given task starts or ends.

     * If the task does not have that date set, compute it by using a relative
     * offset (as defined by the task) in the current year. All time
     * components are set to zero in such case.
     *
     * @param {CMS.Models.TaskGroupTask} instance - the Task to read the
     *   date from
     * @param {string} type - which Task date to read (either "start" or "end")
     *
     * @return {moment} - the date read from the task
     */
    getTaskDate: function (instance, type) {
      let month = instance['relative_' + type + '_month'];
      let day = instance['relative_' + type + '_day'];

      let value = instance[type + '_date'];
      if (value) {
        return moment.utc(value);
      }

      value = moment.utc().set({hour: 0, minute: 0, second: 0, millisecond: 0});

      if (month) {
        value.month(month - 1);  // expects a zero-based month value
      }

      day = Math.min(day, value.daysInMonth());  // prevent days overflow
      value.date(day);

      return value;
    },

    events: {
      ' sortupdate': function (el, ev, ui) {
        let mapping = this.scope.attr('mapping');
        let instanceIndex = _.indexBy(_.pluck(mapping, 'instance'), 'id');

        let instances = _.map(ui.item.parent()
          .children('.task_group_tasks__list-item'), function (el) {
            return instanceIndex[$(el).data('object-id')];
        });

        let targetIndex = _.findIndex(instances, {
          id: ui.item.data('object-id')
        });

        let nexts = []; // index for constant time next element lookup
        let dirty = []; // instances to be saved
        instances[targetIndex].attr('sort_index', null);
        nexts[instances.length] = Number.MAX_SAFE_INTEGER.toString();
        _.eachRight(instances, function (instance, index) {
          nexts[index] = instance.sort_index || nexts[index + 1];
        });

        // in most cases this will only update sort_index for targetIndex
        // but will also correctly resolve missing or duplicate sort_index-es
        _.each(instances, function (instance, index) {
          let prev;
          let next;
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
          let index = instance.sort_index;
          return instance.refresh().then(function (instance) {
            instance.attr('sort_index', index);
            instance.save();
          });
        });
      }
    }
  });
})(window.can, window.can.$);
