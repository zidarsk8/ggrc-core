/*!
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC.Components.mappingTreeView', function () {
  'use strict';

  var unsortedArray = [
    {
      value: 1,
      field: 'a'
    },
    {
      value: 4,
      field: 'd'
    },
    {
      value: 3,
      field: 'c'
    },
    {
      value: 2,
      field: 'b'
    }
  ];
  var sortedAsc = _.sortByOrder(unsortedArray, 'field');
  var sortedDesc = _.sortByOrder(unsortedArray, 'field', 'desc');
  var Component;  // the component under test

  beforeAll(function () {
    Component = GGRC.Components.get('mappingTreeView');
  });

  describe('_sortObjects() method', function () {
    var method;
    var scope;

    beforeAll(function () {
      scope = new can.Map({
        scope: {
          sortField: null
        }
      });
      method = Component.prototype._sortObjects.bind(scope);
    });

    it('returns unsorted array when sortField is not defined', function () {
      expect(method(unsortedArray)).toEqual(unsortedArray);
    });

    it('returns asc sorted array when sortField is defined', function () {
      scope.attr('scope.sortField', 'field');
      expect(method(unsortedArray)).toEqual(sortedAsc);
    });

    it('returns desc sorted array when sortField and sortOrder are defined',
      function () {
        scope.attr('scope.sortField', 'field');
        scope.attr('scope.sortOrder', 'desc');
        expect(method(unsortedArray)).toEqual(sortedDesc);
      });
  });
});
