/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import Component from '../mapping-tree-view';

describe('mapping-tree-view component', function () {
  'use strict';

  let unsortedArray = [
    {
      value: 1,
      field: 'a',
    },
    {
      value: 4,
      field: 'd',
    },
    {
      value: 3,
      field: 'c',
    },
    {
      value: 2,
      field: 'b',
    },
  ];
  let sortedAsc = _.orderBy(unsortedArray, 'field');
  let sortedDesc = _.orderBy(unsortedArray, 'field', 'desc');

  describe('_sortObjects() method', function () {
    let method;
    let viewModel;

    beforeAll(function () {
      viewModel = new can.Map({
        viewModel: {
          sortField: null,
        },
      });
      method = Component.prototype._sortObjects.bind(viewModel);
    });

    it('returns unsorted array when sortField is not defined', function () {
      expect(method(unsortedArray)).toEqual(unsortedArray);
    });

    it('returns asc sorted array when sortField is defined', function () {
      viewModel.attr('viewModel.sortField', 'field');
      expect(method(unsortedArray)).toEqual(sortedAsc);
    });

    it('returns desc sorted array when sortField and sortOrder are defined',
      function () {
        viewModel.attr('viewModel.sortField', 'field');
        viewModel.attr('viewModel.sortOrder', 'desc');
        expect(method(unsortedArray)).toEqual(sortedDesc);
      });
  });
});
