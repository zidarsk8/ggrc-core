/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.repeatOnSummary', function () {
  'use strict';

  var viewModel;

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('repeatOnSummary');
  });

  describe('unitText getter', function () {
    var unitOptions;
    beforeAll(function () {
      unitOptions = GGRC.Workflow.unitOptions;
      GGRC.Workflow.unitOptions = [
        {
          title: 'Daily',
          value: 'Day',
          plural: 'days',
          singular: 'day'},
        {
          title: 'Weekly',
          value: 'Week',
          plural: 'weeks',
          singular: 'week'},
        {
          title: 'Monthly',
          value: 'Month',
          plural: 'months',
          singular: 'month'}];
    });

    afterAll(function () {
      GGRC.Workflow.unitOptions = unitOptions;
    });

    it('returns empty text when unit is not specified', function () {
      var result;

      result = viewModel.attr('unitText');

      expect(result).toBe('');
    });

    it('returns empty text when incorrect unit specified', function () {
      var result;
      viewModel.attr('unit', 'Hour');

      result = viewModel.attr('unitText');

      expect(result).toBe('');
    });

    it('returns appropriate when correct unit specified', function () {
      var result;
      viewModel.attr('unit', 'Week');

      result = viewModel.attr('unitText');

      expect(result).toBe('week');
    });

    it('returns appropriate when correct unit specified', function () {
      var result;
      viewModel.attr('unit', 'Week');
      viewModel.attr('repeatEvery', 4);

      result = viewModel.attr('unitText');

      expect(result).toBe('4 weeks');
    });
  });
});
