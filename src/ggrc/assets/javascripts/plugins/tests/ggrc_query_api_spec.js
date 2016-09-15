/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('GGRC Utils Query API', function () {
  describe('buildParams() method', function () {
    var relevant;
    var objectName;
    var paging;
    var method;

    beforeEach(function () {
      paging = {
        current: 1,
        total: null,
        pageSize: 10,
        filter: '',
        count: 6
      };

      method = GGRC.Utils.QueryAPI.buildParams;
    });

    describe('Assessment related to Audit', function () {
      beforeEach(function () {
        relevant = {type: 'Audit', id: 1};
        objectName = 'Assessment';
      });

      it('return default params for paging request', function () {
        var result = method(objectName, paging, relevant)[0];

        expect(result.object_name).toEqual('Assessment');
        expect(result.limit).toEqual([0, 10]);
        expect(result.filters.expression.object_name).toEqual('Audit');
      });

      it('return limit for 3rd page', function () {
        var result;
        paging.current = 3;
        paging.pageSize = 50;

        result = method(objectName, paging, relevant)[0];

        expect(result.limit).toEqual([100, 150]);
      });
    });

    describe('Request related to Assessment', function () {
      beforeEach(function () {
        relevant = {
          id: 1,
          type: 'Assessment'
        };
        objectName = 'Request';
      });

      it('return default params for paging request', function () {
        var result = method(objectName, paging, relevant)[0];

        expect(result.object_name).toEqual('Request');
        expect(result.limit).toEqual([0, 10]);
        expect(result.filters.expression.object_name).toEqual('Assessment');
      });

      it('return expression for filter', function () {
        var filterResult;
        paging.filter = 'status="in progress"';

        filterResult =
          method(objectName, paging, relevant)[0].filters.expression.right;

        expect(filterResult.left).toEqual('status');
        expect(filterResult.right).toEqual('in progress');
        expect(filterResult.op.name).toEqual('=');
      });
    });

    describe('Correct data for filter expression', function () {
      beforeEach(function () {
        relevant = {
          id: 28,
          type: 'foo',
          operation: 'op'
        };
        objectName = 'bar';
      });

      it('return correct ids', function () {
        var result = method(objectName, paging, relevant)[0];

        expect(result.filters.expression.ids.length).toEqual(1);
        expect(result.filters.expression.ids).toContain('28');
      });
    });

    describe('Assessments owned by the Person', function () {
      beforeEach(function () {
        relevant = {
          id: 1,
          type: 'Person',
          operation: 'owned'
        };
        objectName = 'Assessment';
      });

      it('return owned as operation type', function () {
        var result = method(objectName, paging, relevant)[0];

        expect(result.object_name).toEqual('Assessment');
        expect(result.filters.expression.object_name).toEqual('Person');
        expect(result.filters.expression.op.name).toEqual('owned');
      });
    });
  });
});
