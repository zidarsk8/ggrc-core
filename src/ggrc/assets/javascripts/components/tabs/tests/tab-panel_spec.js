/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.tabPanel', function () {
  'use strict';

  var viewModel;

  describe('#addPanel', function () {
    beforeEach(function () {
      viewModel = GGRC.Components.getViewModel('tabPanel');
      viewModel.addPanel();
    });

    it('should add viewModel reference to the Panels List', function () {
      expect(viewModel.attr('panels').indexOf(viewModel) > -1).toBe(true);
    });
  });

  describe('#removePanel', function () {
    beforeEach(function () {
      viewModel = GGRC.Components.getViewModel('tabPanel');
      viewModel.addPanel();
      viewModel.removePanel();
    });

    it('should remove viewModel reference from the Panels List', function () {
      expect(viewModel.attr('panels').indexOf(viewModel) < 0).toBe(true);
    });

    it('should not do  if no panel from the Panels List', function () {
      viewModel.removePanel();
      expect(viewModel.attr('panels').indexOf(viewModel) < 0).toBe(true);
    });
  });
});
