/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

describe('CMS.Controllers.TreeView', function () {
  'use strict';

  var Ctrl;  // the controller under test

  beforeAll(function () {
    Ctrl = CMS.Controllers.TreeView;
  });

  describe('init() method', function () {
    var ctrlInst;  // fake controller instance
    var dfdSingleton;
    var method;
    var options;
    var $element;

    beforeEach(function () {
      options = {};
      $element = $('<div></div>');

      ctrlInst = {
        element: $element,
        widget_hidden: jasmine.createSpy('widget_hidden'),
        widget_shown: jasmine.createSpy('widget_shown'),
        options: new can.Map(options)
      };

      method = Ctrl.prototype.init.bind(ctrlInst);

      dfdSingleton = new can.Deferred();
      spyOn(
        CMS.Models.DisplayPrefs, 'getSingleton'
      ).and.returnValue(dfdSingleton);
    });

    // test cases here...
  });

  describe('_buildRequestParams() method', function () {
    var ctrlInst;
    var method;

    beforeEach(function () {
      ctrlInst = {
        options: new can.Map({
          parent_instance: {},
          model: {},
          filter: '',
          paging: {
            current: 1,
            total: null,
            pageSize: 10,
            count: 6
          }
        })
      };

      method = Ctrl.prototype._buildRequestParams.bind(ctrlInst);
    });

    describe('Assessment related to Audit', function () {
      beforeEach(function () {
        ctrlInst.options.parent_instance = {
          id: 1,
          type: 'Audit'
        };
        ctrlInst.options.model.shortName = 'Assessment';
      });

      it('return default params for paging request', function () {
        var result = method()[0];

        expect(result.object_name).toEqual('Assessment');
        expect(result.limit).toEqual([0, 10]);
        expect(result.filters.expression.object_name).toEqual('Audit');
      });

      it('return limit for 3rd page', function () {
        var result;
        ctrlInst.options.paging.current = 3;
        ctrlInst.options.paging.pageSize = 50;

        result = method()[0];

        expect(result.limit).toEqual([100, 150]);
      });
    });

    describe('Request related to Assessment', function () {
      beforeEach(function () {
        ctrlInst.options.parent_instance = {
          id: 1,
          type: 'Assessment'
        };
        ctrlInst.options.model.shortName = 'Request';
      });

      it('return default params for paging request', function () {
        var result = method()[0];

        expect(result.object_name).toEqual('Request');
        expect(result.limit).toEqual([0, 10]);
        expect(result.filters.expression.object_name).toEqual('Assessment');
      });

      it('return expression for filter', function () {
        var filterResult;
        ctrlInst.options.attr('filter', 'status="in progress"');

        filterResult = method()[0].filters.expression.right;

        expect(filterResult.left).toEqual('status');
        expect(filterResult.right).toEqual('in progress');
        expect(filterResult.op.name).toEqual('=');
      });
    });
  });

  describe('_verifyRelationship() method', function () {
    var ctrlInst;
    var method;
    var relationship;

    beforeEach(function () {
      ctrlInst = {
        options: new can.Map({
          model: {
            shortName: 'foo'
          }
        })
      };

      relationship = new CMS.Models.Relationship();

      method = Ctrl.prototype._verifyRelationship.bind(ctrlInst);
    });

    it('wrong relationship', function () {
      var result;

      relationship.source = {type: 'bar'};
      relationship.destination = {type: 'baz'};

      result = method(relationship);

      expect(result).toBeFalsy();
    });

    it('right relationship', function () {
      var result;

      relationship.source = {type: 'bar'};
      relationship.destination = {type: 'foo'};

      result = method(relationship);

      expect(result).toBeTruthy();
    });
  });
});
