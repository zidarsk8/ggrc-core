/*!
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.revisionLogData', function () {
  'use strict';

  var viewModel;

  beforeAll(function () {
    viewModel = GGRC.Components.getViewModel('revisionLogData');
  });

  afterAll(function () {
    viewModel = GGRC.Components.getViewModel('revisionLogData');
  });

  describe('isObject', function () {
    it('return true if data value is object', function () {
      viewModel.attr('data', {});
      expect(viewModel.attr('isObject')).toEqual(true);
    });
  });
});
