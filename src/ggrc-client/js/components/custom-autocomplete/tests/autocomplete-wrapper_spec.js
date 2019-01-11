/*
 Copyright (C) 2018 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import baseAutocompleteWrapper from '../autocomplete-wrapper';
import * as QueryAPI from '../../../plugins/utils/query-api-utils';
import RefreshQueue from '../../../models/refresh_queue';
import {getInstance} from '../../../plugins/utils/models-utils';
import Label from '../../../models/service-models/label';

describe('autocomplete-wrapper viewModel', () => {
  let viewModel;

  beforeEach(() => {
    viewModel = baseAutocompleteWrapper();
  });

  describe('getResult() method', () => {
    let response;
    let deferred;
    let stubs;
    let filterResult;
    let fullObjects;
    let currentValueUnique;
    const event = {
      type: 'inputChanged',
      value: 'e',
    };

    beforeEach(() => {
      response = {};
      deferred = new $.Deferred();
      stubs = [];
      filterResult = [];
      fullObjects = [];
      currentValueUnique = true;

      spyOn(viewModel, 'requestItems')
        .and.returnValue(deferred.resolve(response));
      spyOn(viewModel, 'getStubs').and.returnValue(stubs);
      spyOn(viewModel, 'filterResult').and.returnValue(filterResult);
      spyOn(viewModel, 'getFullObjects').and.returnValue(fullObjects);
      spyOn(viewModel, 'isCurrentValueUnique')
        .and.returnValue(currentValueUnique);
    });

    it('should call "requestItems" method', () => {
      viewModel.getResult(event);
      expect(viewModel.requestItems).toHaveBeenCalledWith(event.value);
    });

    it('should call "getStubs" method', () => {
      viewModel.getResult(event);
      expect(viewModel.getStubs).toHaveBeenCalledWith(response);
    });

    it('should call "filterResult" method', () => {
      viewModel.getResult(event);
      expect(viewModel.filterResult).toHaveBeenCalledWith(stubs);
    });

    it('should call "getFullObjects" method', () => {
      viewModel.getResult(event);
      expect(viewModel.getFullObjects).toHaveBeenCalledWith(filterResult);
    });

    it('should assign event value to "currentValue', () => {
      viewModel.getResult(event);

      expect(viewModel.attr('currentValue')).toEqual(event.value);
    });

    it('should set "result" attribute', () => {
      viewModel.getResult(event);

      expect(viewModel.attr('result'))
        .toEqual(jasmine.arrayContaining(fullObjects));
    });

    it('should set "showNewValue" attribute to true', () => {
      viewModel.attr('showNewValue', false);

      viewModel.getResult(event);

      expect(viewModel.attr('showNewValue')).toBe(true);
    });

    it('should set "showResults" attribute to true', () => {
      viewModel.attr('showResults', false);

      viewModel.getResult(event);

      expect(viewModel.attr('showResults')).toBe(true);
    });
  });

  describe('requestItems() method', () => {
    it('should call "buildRelevantIdsQuery" method', () => {
      const objName = 'model';
      const queryField = 'query';
      const value = 'word';
      const filter = {
        expression: {
          left: queryField,
          op: {name: '~'},
          right: value,
        },
      };

      viewModel.attr('modelName', objName);
      viewModel.attr('queryField', queryField);

      spyOn(QueryAPI, 'buildRelevantIdsQuery');
      spyOn(QueryAPI, 'batchRequests');

      viewModel.requestItems(value);

      expect(QueryAPI.buildRelevantIdsQuery)
        .toHaveBeenCalledWith(objName, {}, null, filter);
    });

    it('should return request result', () => {
      const fakeResponseArr = [];

      spyOn(QueryAPI, 'buildRelevantIdsQuery');
      spyOn(QueryAPI, 'batchRequests').and.returnValue(fakeResponseArr);

      const responseArr = viewModel.requestItems('word');

      expect(responseArr).toEqual(fakeResponseArr);
    });
  });

  describe('getStubs() method', () => {
    let name;
    let ids;

    beforeEach(() => {
      name = 'Label';
      ids = [7, 9];
    });

    it('should return stubs from ids', (done) => {
      const responseArr = {
        Label: {
          count: 2,
          ids: ids,
          object_name: name,
          total: 2,
        },
      };

      const fakeRes = [
        getInstance(name, ids[0]),
        getInstance(name, ids[1]),
      ];

      viewModel.attr('modelName', name);
      viewModel.attr('modelConstructor', Label);

      viewModel.getStubs(responseArr).done((res) => {
        expect(res).toEqual(fakeRes);
        done();
      });
    });

    it('should return empty array when items list is empty', (done) => {
      const responseArr = {
        Label: {
          count: 0,
          ids: [],
          object_name: name,
          total: 0,
        },
      };
      const fakeRes = [];

      viewModel.attr('modelName', name);
      viewModel.getStubs(responseArr).done((res) => {
        expect(res).toEqual(fakeRes);
        done();
      });
    });
  });

  describe('getFullObjects() method', () => {
    let result;

    beforeEach(() => {
      result = [{}, {k: 1}];
      spyOn(RefreshQueue.prototype, 'enqueue');
    });

    it('should call "enqueue" method from RefreshQueue object', () => {
      viewModel.getFullObjects(result);
      spyOn(RefreshQueue.prototype, 'trigger');

      expect(RefreshQueue.prototype.enqueue)
        .toHaveBeenCalledTimes(result.length);

      result.forEach((item) => {
        expect(RefreshQueue.prototype.enqueue).toHaveBeenCalledWith(item);
      });
    });

    it('should call "trigger" method from RefreshQueue object', () => {
      spyOn(RefreshQueue.prototype, 'trigger')
        .and.returnValue(new $.Deferred());

      viewModel.getFullObjects(result);

      expect(RefreshQueue.prototype.trigger).toHaveBeenCalled();
    });

    it('should resolve returned deferred after "trigger" is done', (done) => {
      const data = [{a: 1}, {b: 2}];
      spyOn(RefreshQueue.prototype, 'trigger')
        .and.returnValue(new $.Deferred().resolve(data));

      viewModel.getFullObjects(result).done((objs) => {
        expect(objs).toEqual(data);
        done();
      });
    });
  });

  describe('filterResult() method', () => {
    it('should return not changed result if objectsToExclude is empty', () => {
      const fakeResult = [{}, {k: 1}];
      viewModel.attr('objectsToExclude', []);

      const result = viewModel.filterResult(fakeResult);

      expect(result).toEqual(fakeResult);
    });

    it('should return filtered result if objectsToExclude is not empty', () => {
      const objectsToExclude = [{id: 2}, {id: 3}, {id: 4}];
      const data = [{id: 3}, {id: 5}, {id: 7}];
      const fakeResult = [{id: 5}, {id: 7}];
      viewModel.attr('objectsToExclude', objectsToExclude);

      const result = viewModel.filterResult(data);

      expect(result).toEqual(fakeResult);
    });
  });

  describe('isCurrentValueUnique() method', () => {
    it('should return true when collection does not contain currentValue',
      () => {
        const result = [{name: 'rrr'}, {name: 'rrrtt'}];
        viewModel.attr('objectsToExclude', []);
        viewModel.attr('currentValue', 'R');

        const isCurentValue = viewModel.isCurrentValueUnique(result);

        expect(isCurentValue).toBe(true);
      });

    it('should return false when collection contains currentValue', () => {
      const result = [{name: 'r'}, {name: 'rrrtt'}];
      viewModel.attr('objectsToExclude', []);
      viewModel.attr('currentValue', 'R');

      const isCurentValue = viewModel.isCurrentValueUnique(result);

      expect(isCurentValue).toBe(false);
    });

    it('should return false when "objectsToExclude" contains currentValue',
      () => {
        const result = [{name: 'rdsf'}, {name: 'rrrtt'}];
        const objectsToExclude = [{name: 'ggd'}, {name: 'r'}];

        viewModel.attr('objectsToExclude', objectsToExclude);
        viewModel.attr('currentValue', 'R');

        const isCurentValue = viewModel.isCurrentValueUnique(result);

        expect(isCurentValue).toBe(false);
      });
  });
});
