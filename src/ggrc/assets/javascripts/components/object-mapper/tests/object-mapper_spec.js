/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.objectMapper', function () {
  'use strict';

  var Component;
  var events;
  var scope;
  var handler;
  var helpers;

  beforeAll(function () {
    Component = GGRC.Components.get('objectMapper');
    events = Component.prototype.events;
    helpers = Component.prototype.helpers;
  });
  beforeEach(function () {
    scope = GGRC.Components.getViewModel('objectMapper');
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
      it('returns true if it is saving', function () {
        scope.attr('mapper.is_saving', true);
        expect(scope.isLoadingOrSaving()).toEqual(true);
      });
      it('returns true if mapper is loading', function () {
        scope.attr('mapper.is_loading', true);
        expect(scope.isLoadingOrSaving()).toEqual(true);
      });
      it('returns false if page is not loading, it is not saving,' +
      ' type change is not blocked and mapper is not loading', function () {
        scope.attr('mapper.is_saving', false);
        scope.attr('mapper.is_loading', false);
        expect(scope.isLoadingOrSaving()).toEqual(false);
      });
    });
  });

  describe('".create-control modal:success" event', function () {
    var element;
    var spyObj;

    beforeEach(function () {
      scope.attr('mapper', {
        newEntries: []
      });
      spyObj = {
        showNewEntries: jasmine.createSpy()
      };
      element = {
        find: function () {
          return {
            scope: function () {
              return spyObj;
            }
          };
        }
      };
      handler = events['.create-control modal:success'];
    });

    it('adds model to mapper.newEntries', function () {
      handler.call({
        scope: scope,
        element: element
      }, {}, {}, 'model');
      expect(scope.attr('mapper.newEntries').length).toEqual(1);
      expect(scope.attr('mapper.newEntries')[0]).toEqual('model');
    });

    it('calls showNewEntries from mapper-results', function () {
      handler.call({
        scope: scope,
        element: element
      }, {}, {}, 'model');
      expect(spyObj.showNewEntries).toHaveBeenCalled();
    });
  });

  describe('".create-control click" event', function () {
    beforeEach(function () {
      scope.attr('mapper', {});
      handler = events['.create-control click'];
    });

    it('sets empty array to mapper.newEntries', function () {
      handler.call({scope: scope});
      expect(scope.attr('mapper.newEntries').length)
        .toEqual(0);
    });
  });

  describe('".create-control modal:added" event', function () {
    beforeEach(function () {
      scope.attr('mapper', {newEntries: []});
      handler = events['.create-control modal:added'];
    });

    it('adds model to mapper.newEntries', function () {
      handler.call({scope: scope}, {}, {}, 'model');
      expect(scope.attr('mapper.newEntries').length).toEqual(1);
      expect(scope.attr('mapper.newEntries')[0]).toEqual('model');
    });
  });

  describe('"{window} modal:dismiss" event', function () {
    var options;
    var spyObj;
    var element;

    beforeEach(function () {
      scope.attr('mapper', {
        join_object_id: 123,
        newEntries: [1]
      });
      spyObj = {
        showNewEntries: function () {}
      };
      element = {
        find: function () {
          return {
            scope: function () {
              return spyObj;
            }
          };
        }
      };
      spyOn(spyObj, 'showNewEntries');
      handler = events['{window} modal:dismiss'];
    });

    it('calls showNewEntries from mapper-results' +
    'if there are newEntries and ids are equal', function () {
      options = {
        uniqueId: 123
      };
      handler.call({
        scope: scope,
        element: element
      }, {}, {}, options);
      expect(spyObj.showNewEntries).toHaveBeenCalled();
    });

    it('does not call showNewEntries from mapper-results' +
      'if there are newEntries and ids are not equal', function () {
      options = {
        uniqueId: 321
      };
      handler.call({
        scope: scope,
        element: element
      }, {}, {}, options);
      expect(spyObj.showNewEntries).not.toHaveBeenCalled();
    });

    it('does not calls showNewEntries from mapper-results' +
    'if there are no newEntries', function () {
      scope.attr('mapper.newEntries', []);
      options = {
        uniqueId: 123
      };
      handler.call({
        scope: scope,
        element: element
      }, {}, {}, options);
      expect(spyObj.showNewEntries).not.toHaveBeenCalled();
    });
  });

  describe('"inserted" event', function () {
    var that;

    beforeEach(function () {
      scope.attr('mapper', {
        selected: [1, 2, 3],
        entries: [3, 2, 1],
        afterShown: function () {}
      });
      that = {
        scope: scope,
        setModel: jasmine.createSpy('setModel')
      };
      handler = events.inserted;
    });

    it('sets empty array to mapper.selected', function () {
      handler.call(that);
      expect(scope.attr('mapper.selected').length)
        .toEqual(0);
    });
    it('sets empty array to mapper.entries', function () {
      handler.call(that);
      expect(scope.attr('mapper.entries').length)
        .toEqual(0);
    });
    it('calls setModel()', function () {
      handler.call(that);
      expect(that.setModel).toHaveBeenCalled();
    });
  });

  describe('"closeModal" event', function () {
    var element;
    var spyObj;

    beforeEach(function () {
      scope.attr('mapper', {});
      spyObj = {
        trigger: function () {}
      };
      element = {
        find: function () {
          return spyObj;
        }
      };
      spyOn(spyObj, 'trigger');
      handler = events.closeModal;
    });

    it('sets false to mapper.is_saving', function () {
      scope.attr('mapper.is_saving', true);
      handler.call({
        element: element,
        scope: scope
      });
      expect(scope.attr('mapper.is_saving')).toEqual(false);
    });
    it('dismiss the modal', function () {
      handler.call({
        element: element,
        scope: scope
      });
      expect(spyObj.trigger).toHaveBeenCalledWith('click');
    });
  });

  describe('"deferredSave" event', function () {
    var that;
    var spyObj;

    beforeEach(function () {
      spyObj = {
        trigger: function () {}
      };
      scope.attr('mapper', {
        object: 'source'
      });
      scope.attr('deferred_to', {
        controller: {element: spyObj}
      });
      spyObj = scope.attr('deferred_to').controller.element;
      that = {
        scope: scope,
        closeModal: function () {}
      };
      spyOn(that, 'closeModal');
      spyOn(spyObj, 'trigger');
      handler = events.deferredSave;
    });

    it('calls deferredSave', function () {
      handler.call(that);
      expect(spyObj.trigger)
        .toHaveBeenCalledWith('defer:add', [
          {multi_map: true, arr: []},
          {map_and_save: true}
        ]);
    });
    it('calls closeModal', function () {
      handler.call(that);
      expect(that.closeModal).toHaveBeenCalled();
    });
  });

  describe('".modal-footer .btn-map click" handler', function () {
    var that;
    var event;
    var element;
    var callback;

    beforeEach(function () {
      callback = jasmine.createSpy().and.returnValue('expectedResult');
      scope.attr('mapper', {
        callback: callback,
        type: 'type',
        object: 'Program',
        join_object_id: '123',
        selected: []
      });
      spyOn(CMS.Models.Program, 'findInCacheById')
        .and.returnValue('instance');
      event = {
        preventDefault: function () {}
      };
      element = $('<div></div>');
      handler = events['.modal-footer .btn-map click'];
      that = {
        scope: scope,
        closeModal: jasmine.createSpy(),
        deferredSave: jasmine.createSpy().and.returnValue('deferredSave')
      };
      spyOn(window, 'RefreshQueue')
        .and.returnValue({
          enqueue: function () {
            return {
              trigger: jasmine.createSpy()
                .and.returnValue(can.Deferred().resolve())
            };
          }
        });
      spyOn($.prototype, 'trigger');
    });

    it('does nothing if element has class "disabled"', function () {
      var result;
      element.addClass('disabled');
      result = handler.call(that, element, event);
      expect(result).toEqual(undefined);
    });

    it('calls deferredSave if it is deferred', function () {
      var result;
      scope.attr('deferred', true);
      result = handler.call(that, element, event);
      expect(result).toEqual('deferredSave');
    });
    it('calls closeModal()', function () {
      handler.call(that, element, event);
      expect(that.closeModal).toHaveBeenCalled();
    });
    it('triggers error message if fail', function () {
      spyOn($, 'when')
        .and.returnValue(can.Deferred().reject());
      handler.call(that, element, event);
      expect($.prototype.trigger)
        .toHaveBeenCalledWith('ajax:flash', {error: undefined});
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
        setModel: jasmine.createSpy(),
        setBinding: jasmine.createSpy()
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

  describe('get_title() helper', function () {
    var helper;
    beforeEach(function () {
      helper = helpers.get_title;
    });

    it('returns title of parentInstance if parentInstance defined',
      function () {
        var result;
        scope.attr('mapper', {
          parentInstance: {
            title: 'mockTitle'
          }
        });
        result = helper.call(scope);
        expect(result).toEqual('mockTitle');
      });
    it('returns mapper.object if parentInstance undefined',
      function () {
        var result;
        scope.attr('mapper', {
          object: 'mockInstance'
        });
        result = helper.call(scope);
        expect(result).toEqual('mockInstance');
      });
  });

  describe('get_object() helper', function () {
    var helper;

    beforeEach(function () {
      helper = helpers.get_object;
    });

    it('returns type.title_plural if it is defined', function () {
      var result;
      scope.attr('mapper', {
        type: 'Program'
      });
      result = helper.call(scope);
      expect(result).toEqual('Programs');
    });
    it('returns "Objects" if type.title_plural is undefined', function () {
      var result;
      scope.attr('mapper', {});
      result = helper.call(scope);
      expect(result).toEqual('Objects');
    });
  });
});
