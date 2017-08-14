/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  can.Map.extend('GGRC.VM.BaseTreePeopleField', {
    source: null,
    people: [],
    peopleStr: '',
    init: function () {
      this.refreshPeople();
    },
    refreshPeople: function () {
      this.getPeopleList()
        .then(function (data) {
          this.attr('people', data);
          this.attr('peopleStr', data.map(function (item) {
            return item.displayName;
          }).join(', '));
        }.bind(this));
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
              displayName: displayName
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
    }
  });
})(window.can, window.GGRC);
