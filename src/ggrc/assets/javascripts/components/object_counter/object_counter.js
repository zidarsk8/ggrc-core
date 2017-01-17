/*!
   Copyright (C) 2017 Google Inc.
   Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  'use strict';

  /**
   *  Component for object counting. This component relies on backend to
   *  provide specified counter in GGRC.counts namespace for initial load
   *  and performs stub-only findAll query calls only on create/update/delete
   *  events for specific models.
   *
   *  Search values are strings so there's a translation table _getValue that
   *  translates string to value (e.g., 'current_user' gets resolved to
   *  GGRC.current_user.id) before making a GET request.
   *
   *  Search keys and search values lists should be of equal length and
   *  shouldn't be empty (unless that is expected as a query).
   *
   *  `updateCount` function is throttled because of a bug where if user
   *  starts multiple cycles manually `N` times, each subsequent start of a
   *  cycle triggers N events and could spam our server with 10 update requests
   *  if user started 10 cycles without refreshing the page in between.
   *
   *  @param {string} counter - Counter returned by backend in
   *    GGRC.counters.
   *  @param {string} ModelName - Name of a model to perform search on
   *  @param {string} searchKeys - a list semi-colon separated keys to use for
   *    searching
   *  @param {string} searchValues - a list of semi-colon separated values for
   *  corresponding keys that will be used for searching.
   *
   */
  GGRC.Components('ObjectCounter', {
    tag: 'object-counter',
    template: can.view(GGRC.mustache_path +
      '/components/object_counter/object_counter.mustache'),
    scope: {
      counter: '@',
      counterOverdue: '@',
      modelName: '@',
      searchKeys: '@',
      searchValues: '@',
      _getValue: {
        current_user: GGRC.current_user ? GGRC.current_user.id : -1,
        'true': true,
        'false': false
      },
      count: null,
      overdueCount: null,
      initialCount: function () {
        var counter = this.attr('counter');
        var counterOverdue = this.attr('counterOverdue');

        if (_.isUndefined(GGRC.counters[counter])) {
          throw new Error('Counter ' + counter + ' doesn\'t exist');
        }
        this.attr('count', parseInt(GGRC.counters[counter], 10));

        // the "overdue" counter is optional, thus no error
        if (!_.isUndefined(GGRC.counters[counterOverdue])) {
          this.attr(
            'overdueCount',
            parseInt(GGRC.counters[counterOverdue], 10));
        }
      },
      updateCount: _.throttle(function () {
        var searchData = {};
        var i;
        var key;
        var value;
        var data;

        var modelName = this.scope.attr('modelName');
        var keys = this.scope.attr('searchKeys').split(';');
        var values = this.scope.attr('searchValues').split(';');

        if (!GGRC.current_user || !GGRC.current_user.id) {
          return;
        }

        for (i = 0; i < keys.length; i++) {
          key = keys[i].trim();
          value = this.scope._getValue[values[i].trim()] || values[i];
          searchData[key] = value;
        }
        searchData.__stubs_only = true;

        data = CMS.Models[modelName].findAll(searchData);
        data.done(function (objectList) {
          var overdue;
          var utcToday;

          this.scope.attr('count', objectList.length);

          // Calculate overdue objects count, assuming UTC time zone and not
          // taking user's local browser timezone into account.
          utcToday = moment().tz('UTC');

          overdue = _.filter(objectList, function (item) {
            var utcDate;
            if (!item.end_date) {
              return false;  // no end date --> not considered overdue
            }
            utcDate = moment(item.end_date).tz('UTC');
            return utcToday.isAfter(utcDate, 'day');
          });

          this.scope.attr('overdueCount', overdue.length);
        }.bind(this));
      }, 10000)  // See component documentation for explanation
    },
    init: function () {
      var updateEvents = ['created', 'updated', 'destroyed'];
      var model;
      var modelName = this.scope.attr('modelName');
      var keys = this.scope.attr('searchKeys').split(';');
      var values = this.scope.attr('searchValues').split(';');

      if (_.isUndefined(CMS.Models[modelName])) {
        throw new Error('Non-existing model');
      }

      if (keys.length !== values.length) {
        throw new Error('Search keys and values must be of equal length.');
      }

      model = CMS.Models[modelName];

      _.forEach(updateEvents, function (eventName) {
        model.bind(eventName, this.scope.updateCount.bind(this));
      }.bind(this));
    },
    events: {
      inserted: function () {
        this.scope.initialCount();
      }
    }
  });
})(window.can, window.can.$);
