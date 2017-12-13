/*
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import RefreshQueue from '../../models/refresh_queue';

export default can.Map.extend({
  define: {
    stub: {
      type: 'boolean',
      value: true,
    },
  },
  source: null,
  people: [],
  peopleStr: '',
  morePeopleStr: '',
  peopleNum: 5,
  stub: '@',
  init: function () {
    this.refreshPeople();
  },
  refreshPeople: function () {
    this.getPeopleList()
      .then((data) => {
        const peopleStr = data
        .slice(0, this.peopleNum)
        .map((item) => item.displayName)
        .join('\n');

        const morePeopleStr = data.length > this.peopleNum ?
          `\n and ${data.length - this.peopleNum} more` : '';

        this.attr('people', data);
        this.attr('peopleStr', peopleStr);
        this.attr('morePeopleStr', morePeopleStr);
      });
  },
  getPeopleList: function () {
    var sourceList = this.getSourceList();
    var result;
    var deferred = can.Deferred();

    if (!sourceList.length) {
      return deferred.resolve([]);
    }
    this.loadItems(sourceList)
      .then(function (data) {
        result = data.map(function (item) {
          var displayName = item.email;
          return {
            name: item.name,
            email: item.email,
            displayName: displayName,
          };
        });
        deferred.resolve(result);
      })
      .fail(function () {
        deferred.resolve([]);
      });

    return deferred;
  },
  getSourceList: function () {
    console.warn('Function "getSourceList" is not implemented,' +
      'please implement');
    return [];
  },
  loadItems: function (items) {
    var rq = new RefreshQueue();

    can.each(items, function (item) {
      rq.enqueue(CMS.Models.Person.model(item));
    });

    return rq.trigger();
  },
});
