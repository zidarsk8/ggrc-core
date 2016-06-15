/*!
 Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: urban@reciprocitylabs.com
 Maintained By: urban@reciprocitylabs.com
 */

(function (can, $) {
  'use strict';

  /**
   *  Component for object counting. You can specify a model, a list of search
   *  keys and a list of search values. Lengths should be equal and
   *  key-value pair should be on the same place in the semicolon-separated
   *  list.
   *
   *  Search values are strings so there's a translation table getValue that
   *  translates string to value (e.g., 'current_user' gets resolved to
   *  GGRC.current_user.id) before making a GET request.
   *
   *  @param {CMS.Models} Model - Model to perform search on
   *  @param {string} searchKeys - a list semi-colon separated keys to use for
   *    searching
   *  @param {string} searchValues - a list of somi-colon separated values for
   *  corresponding keys that will be used for searching.
   */
  GGRC.Components('ObjectCounter', {
    tag: 'object-counter',
    template: can.view(GGRC.mustache_path +
      '/components/object_counter/object_counter.mustache'),
    scope: {
      model: '@',
      searchKeys: '@',
      searchValues: '@',
      count: '@',
      getValue: {
        current_user: GGRC.current_user.id,
        'true': true,
        'false': false
      },
      updateCount: function () {
        var searchData = {};
        var i;
        var key;
        var value;
        var data;

        var model = this.attr('model');
        var keys = this.attr('searchKeys').split(';');
        var values = this.attr('searchValues').split(';');

        if (!GGRC.current_user || !GGRC.current_user.id) {
          return;
        }

        if (keys.length !== values.length) {
          throw new Error('Search keys and values must be of equal length.');
        }

        if (_.isUndefined(CMS.Models[model])) {
          throw new Error('Non-existing model');
        }

        for (i = 0; i < keys.length; i++) {
          key = keys[i].trim();
          value = this.getValue[values[i].trim()] || values[i];
          searchData[key] = value;
        }

        data = CMS.Models[model].findAll(searchData);
        data.done(function (objectList) {
          this.attr('count', objectList.length);
        }.bind(this));
      }
    },
    events: {
      inserted: function () {
        this.scope.updateCount();
      }
    }
  });
})(window.can, window.can.$);
