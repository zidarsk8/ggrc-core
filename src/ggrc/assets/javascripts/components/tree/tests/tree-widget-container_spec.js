/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.treeWidgetContainer', function () {
  'use strict';

  var vm;

  beforeEach(function () {
    vm = GGRC.Components.getViewModel('treeWidgetContainer');
  });

  describe('onSort() method', function () {
    var onSort;

    beforeEach(function () {
      onSort = vm.onSort.bind(vm);
      vm.attr('pageInfo.count', 3);

      spyOn(vm, 'loadItems');
    });

    it('sets current order properties', function () {
      onSort({
        field: 'col1'
      });

      expect(vm.attr('sortingInfo.sortBy')).toEqual('col1');
      expect(vm.attr('sortingInfo.sortDirection')).toEqual('desc');
      expect(vm.attr('pageInfo.current')).toEqual(1);
      expect(vm.loadItems).toHaveBeenCalled();
    });

    it('changes sortDirection for current column', function () {
      vm.attr('sortingInfo', {
        sortBy: 'field',
        sortDirection: 'desc'
      });
      onSort({
        field: 'field'
      });

      expect(vm.attr('sortingInfo.sortBy')).toEqual('field');
      expect(vm.attr('sortingInfo.sortDirection')).toEqual('asc');
      expect(vm.attr('pageInfo.current')).toEqual(1);
      expect(vm.loadItems).toHaveBeenCalled();
    });

    it('changes sortBy property', function () {
      vm.attr('sortingInfo', {
        sortBy: 'field1',
        sortDirection: 'asc'
      });
      onSort({
        field: 'newField'
      });

      expect(vm.attr('sortingInfo.sortBy')).toEqual('newField');
      expect(vm.attr('sortingInfo.sortDirection')).toEqual('desc');
      expect(vm.attr('pageInfo.current')).toEqual(1);
      expect(vm.loadItems).toHaveBeenCalled();
    });
  });

  describe('loadItems() method', function () {
    var loadItems;

    beforeEach(function () {
      vm.attr({
        model: {shortName: 'modelName'},
        options: {
          parent_instance: {}
        }
      });
      loadItems = vm.loadItems.bind(vm);
    });

    it('', function (done) {
      spyOn(GGRC.Utils.TreeView, 'loadFirstTierItems')
        .and.returnValue(can.Deferred().resolve({
          total: 100,
          values: []
        }));

      loadItems().then(function () {
        expect(vm.attr('pageInfo.total')).toEqual(100);
        expect(can.makeArray(vm.attr('showedItems'))).toEqual([]);
        done();
      });
    });
  });
});
