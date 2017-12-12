/*
  Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import RefreshQueue from '../../models/refresh_queue';
import template from './templates/tree-people-list-field.mustache';

const TOOLTIP_PEOPLE_LIMIT = 5;

const viewModel = can.Map.extend({
  source: null,
  people: [],
  peopleStr: '',
  init: function () {
    this.refreshPeople();
  },
  refreshPeople: function () {
    this.getPeopleList()
      .then((data) => {
        let peopleStr = data
          .slice(0, TOOLTIP_PEOPLE_LIMIT)
          .map((item) => item.email)
          .join('\n');

        peopleStr += data.length > TOOLTIP_PEOPLE_LIMIT ?
          `\n and ${data.length - TOOLTIP_PEOPLE_LIMIT} more` : '';

        this.attr('people', data);
        this.attr('peopleStr', peopleStr);
      });
  },
  getPeopleList: function () {
    let source = this.attr('source');
    let sourceList = can.isArray(source) ? source : can.makeArray(source);
    let deferred = can.Deferred();
    let emailsReadyList;

    if (!sourceList.length) {
      return deferred.resolve([]);
    }

    emailsReadyList = sourceList.filter((people) => people.email);

    if (emailsReadyList.length === sourceList.length) {
      deferred.resolve(sourceList);
    } else {
      this.loadItems(sourceList)
        .then(function (data) {
          deferred.resolve(data);
        })
        .fail(function () {
          deferred.resolve([]);
        });
    }

    return deferred;
  },
  loadItems: function (items) {
    var rq = new RefreshQueue();

    can.each(items, function (item) {
      rq.enqueue(CMS.Models.Person.model(item));
    });

    return rq.trigger();
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
