/*
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../tree-status-filter';
import * as StateUtils from '../../../plugins/utils/state-utils';


describe('treeStatusFilter', () => {
  let viewModel;

  beforeEach(() => {
    viewModel = new Component.prototype.viewModel();
  });

  describe('setFilter() method', () => {
    const FILTER_STRING = 'Foo Bar Baz';
    beforeEach(() => {
      viewModel.attr('filterStates', [
        {value: 'A'},
        {value: 'B'},
        {value: 'C'},
      ]);
      spyOn(StateUtils, 'statusFilter').and.returnValue(FILTER_STRING);
    });

    it('set empty when all statuses selected', () => {
      viewModel.setFilter(['A', 'B', 'C']);

      expect(viewModel.attr('options.filter')).toEqual('');
    });

    it('set empty when no status selected', () => {
      viewModel.setFilter([]);

      expect(viewModel.attr('options.filter')).toEqual('');
    });

    it('set not empty when some status selected', () => {
      viewModel.setFilter(['A']);

      expect(viewModel.attr('options.filter')).toEqual(FILTER_STRING);
    });
  });

  describe('initializeFilter() mthod', () => {
    beforeEach(() => {
      viewModel.attr('filterStates', [
        {value: 'A', checked: false},
        {value: 'B', checked: false},
        {value: 'C', checked: false},
      ]);
      spyOn(viewModel, 'setFilter');
    });

    it('makes provided options checked', ()=> {
      viewModel.initializeFilter(['A', 'C']);

      expect(viewModel.attr('filterStates').serialize()).toEqual([
        {value: 'A', checked: true},
        {value: 'B', checked: false},
        {value: 'C', checked: true},
      ]);
    });

    it('set passed filters', () => {
      viewModel.initializeFilter(['A', 'C']);

      expect(viewModel.setFilter).toHaveBeenCalledWith(['A', 'C']);
    });
  });

  describe('saveTreeStates() method', () => {
    const filters = ['A', 'B'];
    beforeEach(() => {
      let displayPrefs = jasmine.createSpyObj(['setTreeViewStates']);
      viewModel.attr('displayPrefs', displayPrefs);

      spyOn(viewModel, 'setFilter');
    });

    it('set passed filters', () => {
      viewModel.saveTreeStates(filters);

      expect(viewModel.setFilter).toHaveBeenCalledWith(filters);
    });

    describe('saves filter to display preferences', () => {
      it('if widgetId is provided', () => {
        viewModel.attr('widgetId', 'testId');

        viewModel.saveTreeStates(filters);

        expect(viewModel.attr('displayPrefs').setTreeViewStates)
          .toHaveBeenCalledWith('testId', filters);
      });

      it('if modelName is provided', () => {
        viewModel.attr('modelName', 'testName');

        viewModel.saveTreeStates(filters);

        expect(viewModel.attr('displayPrefs').setTreeViewStates)
          .toHaveBeenCalledWith('testName', filters);
      });
    });
  });
});
