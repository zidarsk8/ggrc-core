/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.advancedSearchMappingCriteria', function () {
  'use strict';

  var viewModel;

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('advancedSearchMappingCriteria');
  });

  describe('criteria set() method', function () {
    it('initializes "criteria.filter" property with new attribute model',
    function () {
      viewModel.attr('criteria', can.Map());

      expect(viewModel.attr('criteria.filter').type).toBe('attribute');
    });

    it('does not intialize "criteria.filter" when it is already initialized',
    function () {
      viewModel.attr('criteria', new can.Map({
        filter: {
          type: 'test'
        }
      }));

      expect(viewModel.attr('criteria.filter').type).toBe('test');
    });
  });

  describe('remove() method', function () {
    it('dispatches "remove" event', function () {
      spyOn(viewModel, 'dispatch');

      viewModel.remove();

      expect(viewModel.dispatch).toHaveBeenCalledWith('remove');
    });
  });

  describe('addRelevant() method', function () {
    it('adds mapping criteria', function () {
      viewModel.attr('criteria', can.Map());

      viewModel.addRelevant();

      expect(viewModel.attr('criteria.mappedTo').type).toBe('mappingCriteria');
    });
  });

  describe('removeRelevant() method', function () {
    it('removes mapping criteria', function () {
      viewModel.attr('criteria', new can.Map({
        mappedTo: {}
      }));

      viewModel.removeRelevant();

      expect(viewModel.attr('criteria.mappedTo')).toBe(undefined);
    });
  });
});
