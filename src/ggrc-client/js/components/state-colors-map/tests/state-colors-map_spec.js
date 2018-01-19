/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.stateColorsMap', function () {
  'use strict';

  let completedState = 'In Progress';
  let completedSuffix = 'inprogress';
  let defaultSuffix = 'notstarted';

  describe('in case state is set as "In Progress"', function () {
    let viewModel;

    beforeEach(function () {
      viewModel = GGRC.Components.getViewModel('stateColorsMap');
    });

    it('suffix property should be "inprogress"', function () {
      viewModel.attr('state', completedState);
      expect(viewModel.attr('suffix')).toBe(completedSuffix);
    });
  });

  describe('in case state is not defined', function () {
    let viewModel;

    beforeEach(function () {
      viewModel = GGRC.Components.getViewModel('stateColorsMap');
    });

    it('suffix property should be "notstarted"', function () {
      viewModel.attr('state', null);
      expect(viewModel.attr('suffix')).toBe(defaultSuffix);
    });
  });
});
