/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.tabContainer', function () {
  'use strict';

  var viewModel;

  describe('#setActivePanel ', function () {
    var scope;
    var secondScope;
    var selectionIndex = 3;

    beforeEach(function () {
      viewModel = GGRC.Components.getViewModel('tabContainer');
      scope = new can.Map({
        tabIndex: selectionIndex,
        titleText: 'Some test value ',
        active: false
      });
      secondScope = new can.Map({
        tabIndex: 1,
        titleText: 'Some test value ',
        active: false
      });
      viewModel.attr('panels').push(scope, secondScope);
      viewModel.setActivePanel(scope.attr('tabIndex'));
    });

    it('should select panel with correct tabIndex', function () {
      expect(viewModel.attr('panels')[0].attr('active')).toBe(true);
      expect(viewModel.attr('panels')[1].attr('active')).toBe(false);
    });
  });

  describe('#setDefaultActivePanel ', function () {
    var scope;
    var secondScope;

    beforeEach(function () {
      viewModel = GGRC.Components.getViewModel('tabContainer');
      scope = new can.Map({
        tabIndex: 0,
        titleText: 'Some test value ',
        active: false
      });
      secondScope = new can.Map({
        tabIndex: 1,
        titleText: 'Some test value ',
        active: false
      });
      viewModel.attr('panels').push(scope, secondScope);
    });

    it('should select the first panel' +
      ' if no selectedTabIndex is defined', function () {
      viewModel.setDefaultActivePanel();

      expect(viewModel.attr('panels')[0].attr('active')).toBe(true);
      expect(viewModel.attr('panels')[1].attr('active')).toBe(false);
    });

    it('should select the panel with tabIndex' +
      ' same as selectedTabIndex', function () {
      viewModel.attr('selectedTabIndex', secondScope.attr('tabIndex'));
      viewModel.setDefaultActivePanel();

      expect(viewModel.attr('panels')[0].attr('active')).toBe(false);
      expect(viewModel.attr('panels')[1].attr('active')).toBe(true);
    });
  });
});
