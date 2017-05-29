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
      isLoading: {},
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
        return GGRC.Utils.QueryAPI
          .buildParam('Document', {}, relevantFilters, [], additionalFilter);
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
      }
    },
    init: function () {
      this.viewModel.loadDocuments();
    }
  });
})(window.can, window.can.$);
