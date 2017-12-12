/*
  Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import RefreshQueue from '../../models/refresh_queue';
import template from './templates/tree-people-list-field.mustache';

const viewModel = can.Map.extend({
  define: {
    stub: {
      type: 'boolean',
      value: true,
    },
  },
  filter: '@',
  source: null,
  people: [],
  peopleStr: '',
  peopleNum: 5,
  stub: '@',
  init: function () {
    this.refreshPeople();
  },
  refreshPeople: function () {
    this.getPeopleList()
      .then((data) => {
        let peopleStr = data
          .slice(0, this.peopleNum)
          .map((item) => item.email)
          .join('\n');

        peopleStr += data.length > this.peopleNum ?
          `\n and ${data.length - this.peopleNum} more` : '';

        this.attr('people', data);
        this.attr('peopleStr', peopleStr);
      });
  },
  getPeopleList: function () {
    var sourceList = this.getSourceList();
    var deferred = can.Deferred();

    if (!sourceList.length) {
      return deferred.resolve([]);
    }
    this.loadItems(sourceList)
      .then(function (data) {
        deferred.resolve(data);
      })
      .fail(function () {
        deferred.resolve([]);
      });

    return deferred;
  },
  loadItems: function (items) {
    var rq = new RefreshQueue();

    can.each(items, function (item) {
      rq.enqueue(CMS.Models.Person.model(item));
    });

    return rq.trigger();
  },
  getSourceList: function () {
    let filter = this.attr('filter');
    let sourceString = 'source';

    if (filter) {
      sourceString += '.' + filter;
    }

    return can.makeArray(this.attr(sourceString));
  },
});

GGRC.Components('treePeopleListField', {
  tag: 'tree-people-list-field',
  template: template,
  viewModel: viewModel,
  events: {
    '{viewModel} source': function () {
      this.viewModel.refreshPeople();
    },
  },
});
