/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC) {
  'use strict';

  GGRC.Components('relatedDocuments', {
    tag: 'related-documents',
    viewModel: {
      instance: {},
      documentType: '@',
      documents: [],
      isLoading: false,
      getDocumentsQuery: function () {
        var relevantFilters = [{
          type: this.attr('instance.type'),
          id: this.attr('instance.id'),
          operation: 'relevant'
        }];
        var additionalFilter = this.attr('documentType') ?
        {
          expression: {
            left: 'document_type',
            op: {name: '='},
            right: this.attr('documentType')
          }
        } :
        [];

        var query = GGRC.Utils.QueryAPI
          .buildParam('Document', {}, relevantFilters, [], additionalFilter);
        query.order_by = [{name: 'created_at', desc: false}];

        return query;
      },
      loadDocuments: function () {
        var self = this;
        var query = this.getDocumentsQuery();

        this.attr('isLoading', true);
        GGRC.Utils.QueryAPI.batchRequests(query).then(function (response) {
          var documents = response.Document.values;
          self.attr('documents').replace(documents);
          self.attr('isLoading', false);
        });
      },
      removeDocument: function (event) {
        var item = event.item;
        var index = this.attr('documents').indexOf(item);
        this.attr('isLoading', true);
        return this.attr('documents').splice(index, 1);
      },
      addDocuments: function (event) {
        var items = event.items;
        this.attr('isLoading', true);
        return this.attr('documents').unshift
          .apply(this.attr('documents'), items);
      }
    },
    init: function () {
      this.viewModel.loadDocuments();
    }
  });
})(window.GGRC, window);
