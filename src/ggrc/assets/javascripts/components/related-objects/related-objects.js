/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, CMS) {
  'use strict';

  var defaultOrderBy = 'created_at';

  can.Component.extend({
    tag: 'related-objects',
    viewModel: {
      define: {
        noRelatedObjectsMessage: {
          type: 'string',
          get: function () {
            return 'No Related ' + this.attr('relatedItemsType') + 's ' +
              'were found';
          }
        },
        isLoading: {
          type: 'boolean',
          value: false
        }
      },
      baseInstance: null,
      relatedObjects: [],
      relatedItemsType: '@',
      orderBy: '@',
      selectedItem: {},
      objectSelectorEl: '.grid-data__action-column button',
      paging: {
        current: 1,
        pageSize: 5,
        pageSizeSelect: [5, 10, 15]
      },
      getParams: function () {
        var id;
        var type;
        var relatedType = this.attr('relatedItemsType');
        var page = this.attr('paging');
        var orderBy = this.attr('orderBy') || defaultOrderBy;
        var isAssessment = this.attr('baseInstance.type') === 'Assessment';
        var isSnapshot = !!this.attr('baseInstance.snapshot');
        var filters;
        var params = {};
        var first;
        var last;

        if (isSnapshot) {
          id = this.attr('baseInstance.snapshot.child_id');
          type = this.attr('baseInstance.snapshot.child_type');
        } else {
          id = this.attr('baseInstance.id');
          type = this.attr('baseInstance.type');
        }

        if (page.current && page.pageSize) {
          first = (page.current - 1) * page.pageSize;
          last = page.current * page.pageSize;
        }
        // Use only "similar" filter for Assessments
        filters = isAssessment ? {
          expression: {
            object_name: type,
            op: {name: 'similar'},
            ids: [id]
          }
        } : {
          expression: {
            left: {
              object_name: type,
              op: {name: 'relevant'},
              ids: [id]
            },
            right: {
              object_name: type,
              op: {name: 'similar'},
              ids: [id]
            },
            op: {name: 'OR'}
          }
        };
        params.data = [{
          limit: [first, last],
          object_name: relatedType,
          order_by: orderBy.split(',').map(function (field) {
            return {name: field, desc: true};
          }),
          filters: filters
        }];
        return params;
      },
      updatePaging: function (total) {
        var count = Math.ceil(total / this.attr('paging.pageSize'));
        this.attr('paging.total', total);
        this.attr('paging.count', count);
      },
      loadRelatedItems: function () {
        var dfd = can.Deferred();
        var params = this.getParams();
        this.attr('isLoading', true);
        GGRC.Utils.QueryAPI
          .makeRequest(params)
          .done(function (responseArr) {
            var relatedType = this.attr('relatedItemsType');
            var data = responseArr[0];
            var values = data[relatedType].values;
            var result = values.map(function (item) {
              return {
                instance: CMS.Models[relatedType].model(item)
              };
            });
            // Update paging object
            this.updatePaging(data[relatedType].total);
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
      setRelatedItems: function () {
        this.attr('relatedObjects').replace(this.loadRelatedItems());
      }
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
      '{viewModel.baseInstance} refreshInstance': function () {
        this.viewModel.setRelatedItems();
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
