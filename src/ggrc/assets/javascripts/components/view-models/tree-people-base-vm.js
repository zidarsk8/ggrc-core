/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

export default can.Map.extend({
  define: {
    stub: {
      type: 'boolean',
      value: true
    }
  },
  source: null,
  people: [],
  peopleStr: '',
  stub: '@',
  init: function () {
    this.refreshPeople();
  },
  refreshPeople: function () {
    this.getPeopleList()
      .then(function (data) {
        this.attr('people', data);
        this.attr('peopleStr', data.map(function (item) {
          return item.email;
        }).join(', '));
      }.bind(this));
  },
  getPeopleList: function () {
    var sourceList = this.getSourceList();
    var deferred = can.Deferred();

    if (!sourceList.length) {
      return deferred.resolve([]);
    }

    if (this.attr('stub')) {
      this.loadItems(sourceList)
        .then(function (data) {
          deferred.resolve(data);
        })
        .fail(function () {
          deferred.resolve([]);
        });
    } else {
      deferred.resolve(sourceList);
    }

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
  }
});
