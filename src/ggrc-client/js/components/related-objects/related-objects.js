/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../sortable-column/sortable-column';
import {REFRESH_RELATED} from '../../events/eventTypes';
import {
  makeRequest,
} from '../../plugins/utils/query-api-utils';
import Pagination from '../base-objects/pagination';

(function (can, GGRC, CMS) {
  'use strict';

  let defaultOrderBy = 'created_at';

  GGRC.Components('relatedObjects', {
    tag: 'related-objects',
    viewModel: {
      define: {
        noRelatedObjectsMessage: {
          type: 'string',
          get: function () {
            return 'No Related ' + this.attr('relatedItemsType') + 's ' +
              'were found';
          },
        },
        isLoading: {
          type: 'boolean',
          value: false,
        },
        paging: {
          value: function () {
            return new Pagination({pageSizeSelect: [5, 10, 15]});
          },
        },
        relatedObjects: {
          Value: can.List,
        },
        predefinedFilter: {
          type: '*',
        },
      },
      baseInstance: null,
      relatedItemsType: '@',
      orderBy: {},
      initialOrderBy: '@',
      selectedItem: {},
      getFilters: function (id, type) {
        let predefinedFilter = this.attr('predefinedFilter');
        let filters;

        let hasSimilar = _.includes(['Assessment', 'Control', 'Objective'],
          this.attr('baseInstance.type'));

        if (predefinedFilter) {
          filters = predefinedFilter;
        } else {
          filters = {
            expression: {
              object_name: type,
              op: hasSimilar ? {name: 'similar'} : {name: 'relevant'},
              ids: [id],
            },
          };
        }
        return filters;
      },
      getParams: function () {
        let id;
        let type;
        let relatedType = this.attr('relatedItemsType');
        let isSnapshot = !!this.attr('baseInstance.snapshot');
        let filters;
        let params = {};

        if (isSnapshot) {
          id = this.attr('baseInstance.snapshot.child_id');
          type = this.attr('baseInstance.snapshot.child_type');
        } else {
          id = this.attr('baseInstance.id');
          type = this.attr('baseInstance.type');
        }
        filters = this.getFilters(id, type);
        params.data = [{
          limit: this.attr('paging.limits'),
          object_name: relatedType,
          order_by: this.getSortingInfo(),
          filters: filters,
        }];
        return params;
      },
      loadRelatedItems: function () {
        let dfd = can.Deferred();
        let params = this.getParams();
        this.attr('isLoading', true);

        makeRequest(params)
          .done(function (responseArr) {
            let relatedType = this.attr('relatedItemsType');
            let data = responseArr[0];
            let values = data[relatedType].values;
            let result = values.map(function (item) {
              return {
                instance: CMS.Models[relatedType].model(item),
              };
            });
            // Update paging object
            this.attr('paging.total', data[relatedType].total);
            dfd.resolve(result);
          }.bind(this))
          .fail(function () {
            dfd.resolve([]);
          })
          .always(function () {
            this.attr('isLoading', false);
          }.bind(this));
        return dfd;
      },
      getSortingInfo: function () {
        let orderBy = this.attr('orderBy');
        let defaultOrder;

        if (!orderBy.attr('field')) {
          defaultOrder = this.attr('initialOrderBy') || defaultOrderBy;
          return defaultOrder.split(',').map(function (field) {
            return {name: field, desc: true};
          });
        }

        return [{
          name: orderBy.attr('field'),
          desc: orderBy.attr('direction') === 'desc'}];
      },
      setRelatedItems: function () {
        this.attr('relatedObjects').replace(this.loadRelatedItems());
      },
    },
    init: function () {
      this.viewModel.setRelatedItems();
    },
    events: {
      '{viewModel.paging} current': function () {
        this.viewModel.setRelatedItems();
      },
      '{viewModel.paging} pageSize': function () {
        this.viewModel.setRelatedItems();
      },
      [`{viewModel.baseInstance} ${REFRESH_RELATED.type}`]:
        function (scope, event) {
          let vm = this.viewModel;

          if (vm.attr('relatedItemsType') === event.model) {
            vm.setRelatedItems();
          }
        },
      '{viewModel.orderBy} changed': function () {
        this.viewModel.setRelatedItems();
      },
    },
  });
})(window.can, window.GGRC, window.CMS);
