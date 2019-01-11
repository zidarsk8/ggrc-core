/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

// Base viewModel for custom autocomplete. Must be extended into component.
// Provides component-wrapper for custom autocomplete.
// Must contain 'autocomplete-results' and 'autocomplete-input' components.

import {
  buildRelevantIdsQuery,
  batchRequests,
} from '../../plugins/utils/query-api-utils';
import RefreshQueue from '../../models/refresh_queue';
import {getInstance} from '../../plugins/utils/models-utils';

export default can.Map.extend({
  currentValue: '',
  modelName: null,
  modelConstructor: null,
  result: [],
  objectsToExclude: [],
  showResults: false,
  showNewValue: false,
  queryField: 'title',
  getResult: function (event) {
    let that = this;
    this.requestItems(event.value)
      .then(that.getStubs.bind(that))
      .then(that.filterResult.bind(that))
      .then(that.getFullObjects.bind(that))
      .then((result) => {
        that.attr('currentValue',
          event.value);
        that.attr('result', result);
        that.attr('showNewValue', that.isCurrentValueUnique(result));
        that.attr('showResults', true);
      });
  },
  // Gets ids of items using QueryAPI
  requestItems: function (value) {
    let queryField = this.attr('queryField');
    let objName = this.attr('modelName');
    let filter = {expression: {
      left: queryField,
      op: {name: '~'},
      right: value,
    }};
    let query = buildRelevantIdsQuery(objName, {}, null, filter);

    return batchRequests(query);
  },
  getStubs: function (responseArr) {
    let objName = this.attr('modelName');
    let ids = responseArr[objName].ids;
    let modelConstructor = this.attr('modelConstructor');

    let res = can.map(ids, function (id) {
      return getInstance(modelConstructor.shortName, id);
    });

    return new $.Deferred().resolve(res);
  },
  getFullObjects: function (result) {
    let defer = new $.Deferred();
    let queue = new RefreshQueue();

    _.forEach(result, (object) => {
      queue.enqueue(object);
    });

    queue.trigger().then((objs) => {
      defer.resolve(objs);
    });

    return defer;
  },
  filterResult: function (result) {
    let objects = this.attr('objectsToExclude');

    result = result.filter((item) => {
      return !_.some(objects, (object) => item.id === object.id);
    });

    return result;
  },
  isCurrentValueUnique: function (result) {
    let objects = this.attr('objectsToExclude').concat(result);
    let currentValue = this.attr('currentValue').toLowerCase();

    return !_.some(objects, (object) =>
      object.name.toLowerCase() === currentValue);
  },
});
