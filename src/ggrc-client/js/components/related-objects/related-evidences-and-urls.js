/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {
  buildParam,
  batchRequests,
} from '../../plugins/utils/query-api-utils';

(function (can, $, _, GGRC) {
  'use strict';

  GGRC.Components('relatedEvidencesAndUrls', {
    tag: 'related-evidences-and-urls',
    viewModel: {
      define: {
        parentInstance: {
          value: {},
        },
      },
      documents: [],
      isLoading: false,
      getDocumentsQuery: function () {
        let documentTypes = [
          CMS.Models.Document.EVIDENCE,
          CMS.Models.Document.URL];
        let relevantFilters = [{
          type: this.attr('parentInstance.type'),
          id: this.attr('parentInstance.id'),
          operation: 'relevant',
        }];
        let includeFilters = {
          keys: [],
          expression: {},
        };
        let query;

        documentTypes.forEach(function (type) {
          includeFilters = GGRC.query_parser.join_queries({
            expression: {
              op: {name: '='},
              left: 'document_type',
              right: type,
            },
            keys: [],
          }, includeFilters, 'OR');
        });

        query =
          buildParam('Document', {}, relevantFilters, [], includeFilters);
        query.order_by = [{name: 'created_at', desc: true}];

        return query;
      },
      loadDocuments: function () {
        let self = this;
        let query = this.getDocumentsQuery();

        this.attr('isLoading', true);
        return batchRequests(query).then(
          function (response) {
            let documents = response.Document.values;
            self.attr('documents').replace(documents);
            self.attr('isLoading', false);
          }
        );
      },
    },
    init: function () {
      this.viewModel.loadDocuments();
    },
  });
})(window.can, window.can.$, window._, window.GGRC);
