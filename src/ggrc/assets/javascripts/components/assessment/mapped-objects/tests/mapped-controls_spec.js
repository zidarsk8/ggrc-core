/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import * as SnapshotUtils from '../../../../plugins/utils/snapshot-utils';
import * as QueryAPI from '../../../../plugins/utils/query-api-utils';

describe('GGRC.Component.assessmentMappedControl', function () {
  'use strict';

  var viewModel;
  var defaultResponseArr = [
    {
      Snapshot: {
        values: []
      }
    }, {
      Snapshot: {
        values: []
      }
    }];
  var noDataResponseArr = defaultResponseArr;
  var params = {
    data: [
      {
        object_name: 'Snapshot',
        filters: {
          expression: {
            left: {
              left: 'child_type',
              op: {name: '='},
              right: 'Objective'},
            op: {name: 'AND'},
            right: {
              object_name: 'Snapshot',
              op: {name: 'relevant'},
              ids: ['1']
            }
          },
          keys: [],
          order_by: {
            keys: [],
            order: '',
            compare: null
          }
        },
        fields: ['revision']
      }, {
        object_name: 'Snapshot',
        filters: {
          expression: {
            left: {
              left: 'child_type',
              op: {name: '='},
              right: 'Regulation'
            },
            op: {name: 'AND'},
            right: {
              object_name: 'Snapshot',
              op: {name: 'relevant'},
              ids: ['1']
            }
          },
          keys: [],
          order_by: {
            keys: [],
            order: '',
            compare: null
          }
        },
        fields: ['revision']
      }]
  };
  var selectedItem = {
    data: {
      id: 1
    }
  };

  beforeEach(function () {
    viewModel = new GGRC.Components
      .getViewModel('assessmentMappedControl');
  });

  describe('loadItems() method', function () {
    var pendingRequest;
    beforeEach(function () {
      pendingRequest = $.Deferred();
      spyOn(SnapshotUtils, 'toObject');
      spyOn(viewModel, 'setItems');
      spyOn(viewModel, 'getParams')
        .and.returnValue(params);
      spyOn(QueryAPI, 'makeRequest')
        .and.returnValue(pendingRequest);
    });

    it('sets default items when control was not selected',
      function () {
        viewModel.loadItems();

        expect(viewModel.setItems)
          .toHaveBeenCalledWith(defaultResponseArr);
      });

    it('sets items when no data returned', function () {
      viewModel.attr('selectedItem', selectedItem);

      viewModel.loadItems();
      expect(viewModel.getParams).toHaveBeenCalled();
      expect(viewModel.attr('isLoading')).toBeTruthy();

      pendingRequest.resolve(noDataResponseArr);
      expect(viewModel.setItems)
        .toHaveBeenCalledWith(noDataResponseArr);
      expect(viewModel.attr('isLoading')).toBeFalsy();
    });

    it('sets items when appropriate data returned', function () {
      var dataResponseArr = [{
        id: 2
      }];
      viewModel.attr('selectedItem', selectedItem);

      viewModel.loadItems();
      expect(viewModel.getParams).toHaveBeenCalled();
      expect(viewModel.attr('isLoading')).toBeTruthy();

      pendingRequest.resolve(dataResponseArr);
      expect(viewModel.setItems)
        .toHaveBeenCalledWith(dataResponseArr);
      expect(viewModel.attr('isLoading')).toBeFalsy();
    });

    it('sets default items when request fails',
      function () {
        viewModel.attr('selectedItem', selectedItem);
        spyOn($.prototype, 'trigger');

        viewModel.loadItems();

        expect(viewModel.attr('isLoading')).toBeTruthy();

        pendingRequest.reject();
        expect($.prototype.trigger)
          .toHaveBeenCalledWith('ajax:flash',
            {error: 'Failed to fetch related objects.'});
        expect(viewModel.setItems)
          .toHaveBeenCalledWith(defaultResponseArr);
        expect(viewModel.attr('isLoading')).toBeFalsy();
      });
  });

  describe('setItems() method', function () {
    var dummyObject = {
      id: 1
    };
    beforeEach(function () {
      spyOn(SnapshotUtils, 'toObject')
        .and.returnValue(dummyObject);
    });

    it('sets empty array when empty response', function () {
      viewModel.setItems(noDataResponseArr);

      expect(viewModel.attr('objectives.length'))
        .toEqual(0);
      expect(viewModel.attr('regulations.length'))
        .toEqual(0);
    });

    it('sets an appropriate items for non empty response',
      function () {
        var response = [
          {
            Snapshot: {
              values: [
                {
                  id: 2
                }]
            }
          },
          {
            Snapshot: {
              values: []
            }
          }];

        viewModel.setItems(response);

        expect(viewModel.attr('objectives.length'))
          .toEqual(1);
        expect(viewModel.attr('objectives.0.id'))
          .toEqual(1);
        expect(viewModel.attr('regulations.length'))
          .toEqual(0);
      });
  });
});
