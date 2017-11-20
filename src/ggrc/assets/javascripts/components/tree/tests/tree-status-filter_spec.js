/*
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../tree-status-filter';
import * as StateUtils from '../../../plugins/utils/state-utils';

const FILTER_STRING = 'Foo Bar Baz';

describe('GGRC.Components.treeStatusFilter', () => {
  let vm;

  beforeEach(() => {
    vm = new Component.prototype.viewModel();

    vm.attr('filterStates', [
      {value: 'A'},
      {value: 'B'},
      {value: 'C'},
    ]);

    spyOn(StateUtils, 'statusFilter').and.returnValue(FILTER_STRING)
  });

  describe('filter property', () => {
    it('is empty when all statuses selected', () => {
      vm.attr('selectedStates', ['A', 'B', 'C']);

      expect(vm.attr('options.filter')).toEqual('');
    });

    it('is empty when no status selected', () => {
      vm.attr('selectedStates', []);

      expect(vm.attr('options.filter')).toEqual('');
    });

    it('not empty when some status selected', () => {
      vm.attr('selectedStates', ['A']);

      expect(vm.attr('options.filter')).toEqual(FILTER_STRING);
    });
  });
});
