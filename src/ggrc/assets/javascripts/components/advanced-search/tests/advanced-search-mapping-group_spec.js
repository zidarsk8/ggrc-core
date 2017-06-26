/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.advancedSearchMappingGroup', function () {
  'use strict';

  var viewModel;

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('advancedSearchMappingGroup');
  });

  describe('addMappingCriteria() method', function () {
    it('adds operator and criteria', function () {
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
    it('removes criteria and operator behind if item is first',
    function () {
      var viewItems;
      viewModel.attr('items', [
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({field: 'first'}),
        GGRC.Utils.AdvancedSearch.create.operator(),
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({field: 'second'})
      ]);
      viewItems = viewModel.attr('items');

      viewModel.removeMappingCriteria(viewItems[0]);

      expect(viewItems.length).toBe(1);
      expect(viewItems[0].type).toBe('mappingCriteria');
      expect(viewItems[0].value.field).toBe('second');
    });

    it('removes criteria and operator in front if item is not first',
    function () {
      var viewItems;
      viewModel.attr('items', [
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({field: 'first'}),
        GGRC.Utils.AdvancedSearch.create.operator(),
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({field: 'second'})
      ]);
      viewItems = viewModel.attr('items');

      viewModel.removeMappingCriteria(viewItems[2]);

      expect(viewItems.length).toBe(1);
      expect(viewItems[0].type).toBe('mappingCriteria');
      expect(viewItems[0].value.field).toBe('first');
    });

    it('removes group if single criteria was removed', function () {
      var viewItems;
      viewModel.attr('items', [
        GGRC.Utils.AdvancedSearch.create.mappingCriteria({field: 'single'})
      ]);
      viewItems = viewModel.attr('items');
      spyOn(viewModel, 'remove');

      viewModel.removeMappingCriteria(viewItems[0]);

      expect(viewModel.remove).toHaveBeenCalled();
    });
  });
});
