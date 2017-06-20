/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.advancedSearchMappingContainer', function () {
  'use strict';

  var viewModel;

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('advancedSearchMappingContainer');
  });

  describe('addMappingCriteria() method', function () {
    it('adds only criteria if list is empty', function () {
      var items;

      viewModel.addMappingCriteria();

      items = viewModel.attr('items');
      expect(items.length).toBe(1);
      expect(items[0].type).toBe('mappingCriteria');
    });

    it('adds operator and criteria if list is not empty', function () {
      var items;
      viewModel.attr('items',
        [GGRC.Utils.AdvancedSearch.create.mappingCriteria()]);
      viewModel.addMappingCriteria();

      items = viewModel.attr('items');
      expect(items.length).toBe(3);
      expect(items[0].type).toBe('mappingCriteria');
      expect(items[1].type).toBe('operator');
      expect(items[2].type).toBe('mappingCriteria');
    });
  });

  describe('removeMappingCriteria() method', function () {
    it('removes criteria and operator in front if item is first',
    function () {
      var viewItems;
      viewModel.attr('items', [
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({objectName: 'first'}),
        GGRC.Utils.AdvancedSearch.create.operator(),
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({objectName: 'second'})
      ]);
      viewItems = viewModel.attr('items');

      viewModel.removeMappingCriteria(viewItems[0]);

      expect(viewItems.length).toBe(1);
      expect(viewItems[0].type).toBe('mappingCriteria');
      expect(viewItems[0].value.objectName).toBe('second');
    });

    it('removes mappingCriteria and operator behind if item is not first',
    function () {
      var viewItems;
      viewModel.attr('items', [
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({objectName: 'first'}),
        GGRC.Utils.AdvancedSearch.create.operator(),
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({objectName: 'second'})
      ]);
      viewItems = viewModel.attr('items');

      viewModel.removeMappingCriteria(viewItems[2]);

      expect(viewItems.length).toBe(1);
      expect(viewItems[0].type).toBe('mappingCriteria');
      expect(viewItems[0].value.objectName).toBe('first');
    });
  });
});
