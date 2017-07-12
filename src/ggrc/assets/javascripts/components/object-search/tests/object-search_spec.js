/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.objectSearch', function () {
  'use strict';

  var Component;
  var events;
  var scope;
  var handler;

  beforeAll(function () {
    Component = GGRC.Components.get('objectSearch');
    events = Component.prototype.events;
  });
  beforeEach(function () {
    scope = GGRC.Components.getViewModel('objectSearch');
  });

  describe('scope() method', function () {
    var el;
    var parentScope;

    beforeEach(function () {
      el = new can.Map();
      parentScope = new can.Map();
    });
    it('returns object with function "isLoadingOrSaving"', function () {
      var result = Component.prototype.scope({}, parentScope, el);
      expect(result.isLoadingOrSaving).toEqual(jasmine.any(Function));
    });

    describe('isLoadingOrSaving() method', function () {
      beforeEach(function () {
        scope = new can.Map(Component.prototype.scope({}, parentScope, el));
      });
      it('returns true if mapper is loading', function () {
        scope.attr('mapper.is_loading', true);
        expect(scope.isLoadingOrSaving()).toEqual(true);
      });
      it('returns false if page is not loading, it is not saving,' +
      ' type change is not blocked and mapper is not loading', function () {
        scope.attr('mapper.is_loading', false);
        expect(scope.isLoadingOrSaving()).toEqual(false);
      });
    });
  });

  describe('"inserted" event', function () {
    var that;

    beforeEach(function () {
      scope.attr('mapper', {
        afterShown: function () {}
      });
      that = {
        scope: scope,
        setModel: jasmine.createSpy('setModel')
      };
      handler = events.inserted;
    });

    it('calls setModel()', function () {
      handler.call(that);
      expect(that.setModel).toHaveBeenCalled();
    });
  });

  describe('"setModel" handler', function () {
    beforeEach(function () {
      scope.attr('mapper', {
        modelFromType: function () {}
      });
      spyOn(scope.mapper, 'modelFromType')
        .and.returnValue('mockModel');
      handler = events.setModel;
    });
    it('sets model to mapper.model', function () {
      handler.call({scope: scope});
      expect(scope.attr('mapper.model')).toEqual('mockModel');
    });
  });

  describe('"{mapper} type" handler', function () {
    var that;
    beforeEach(function () {
      scope.attr('mapper', {
        relevant: [1, 2, 3],
        onSubmit: function () {}
      });
      that = {
        scope: scope,
        setModel: jasmine.createSpy()
      };
      handler = events['{mapper} type'];
    });

    it('sets empty string to mapper.filter', function () {
      handler.call(that);
      expect(scope.attr('mapper.filter')).toEqual('');
    });
    it('sets false to mapper.afterSearch', function () {
      handler.call(that);
      expect(scope.attr('mapper.afterSearch')).toEqual(false);
    });
    it('calls setModel()', function () {
      handler.call(that);
      expect(that.setModel).toHaveBeenCalled();
    });
    it('sets empty array to mapper.relevant if it is not in scope model',
      function () {
        spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
          .and.returnValue(false);
        handler.call(that);
        expect(scope.attr('mapper.relevant').length)
          .toEqual(0);
      });
  });
});
