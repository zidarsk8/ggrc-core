/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.relatedEvidencesAndUrls', function () {
  'use strict';

  let viewModel;
  let instance;

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('relatedEvidencesAndUrls');
    instance = {
      id: '5',
      type: 'Assessment'
    };

    viewModel.attr('parentInstance', instance);
  });

  describe('"getDocumentsQuery" method', function () {
    function checkAdditionFilter(leftDocType, rightDocType) {
      let query;
      let additionFilter;
      query = viewModel.getDocumentsQuery();

      expect(query.filters.expression).toBeDefined();
      additionFilter = query.filters.expression.right;
      expect(additionFilter.left.left).toEqual('document_type');
      expect(additionFilter.left.right).toEqual(leftDocType);
      expect(additionFilter.right.left).toEqual('document_type');
      expect(additionFilter.right.right).toEqual(rightDocType);
    }

    it('should get query for urls and evidences', function () {
      checkAdditionFilter(CMS.Models.Document.URL,
        CMS.Models.Document.EVIDENCE);
    });
  });
});
