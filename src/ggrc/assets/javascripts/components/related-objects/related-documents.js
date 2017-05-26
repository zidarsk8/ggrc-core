/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, $) {
  'use strict';

  GGRC.Components('relatedDocuments', {
    tag: 'related-documents',
    viewModel: {
      instance: null,
      documentType: '@',
      documents: [],
      loadDocuments: function () {
        var self = this;
        var queryApi = GGRC.Utils.QueryAPI;
        var relevantFilters = [{
          type: this.attr('instance.type'),
          id: this.attr('instance.id'),
          operation: 'relevant'
        }];
        var additionalFilter = {
          expression: {
            left: 'document_type',
            op: {name: '='},
            right: this.attr('documentType')
          }
        };
        var query = queryApi
          .buildParam('Document', {}, relevantFilters, [], additionalFilter);

        queryApi.batchRequests(query).then(function (response) {
          var documents = response.Document.values;
          self.attr('documents').replace(documents);
        });
      }
    },
    init: function () {
      this.viewModel.loadDocuments();
    }
  });
})(window.can, window.can.$);
