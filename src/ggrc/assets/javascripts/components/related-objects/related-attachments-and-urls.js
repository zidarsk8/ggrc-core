/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can) {
  'use strict';

  /**
   * Simple wrapper component for related attachments and urls
   */
  can.Component.extend({
    tag: 'related-attachments-and-urls',
    viewModel: {
      define: {
        noRelatedItemMessage: {
          type: String,
          value: function () {
            return '';
          }
        },
        emptyMessage: {
          type: String,
          value: function () {
            return 'None';
          }
        },
        loadingState: {}
      },
      documents: [],
      loadDocuments: function () {
        var self = this;
        var queryApi = GGRC.Utils.QueryAPI;
        var relevantFilters = [{
          type: this.attr('instance.type'),
          id: this.attr('instance.id'),
          operation: 'relevant'
        }];
        var query = queryApi
          .buildParam('Document', {}, relevantFilters, [], []);

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
})(window.can);
