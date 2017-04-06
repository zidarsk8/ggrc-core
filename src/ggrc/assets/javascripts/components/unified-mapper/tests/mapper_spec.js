/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Models.MapperModel', function () {
  'use strict';

  var mapper;

  beforeEach(function () {
    mapper = GGRC.Models.MapperModel();
  });

  describe('get() for mapper.types', function () {
    beforeEach(function () {
      spyOn(mapper, 'initTypes')
        .and.returnValue('types');
    });

    it('returns types', function () {
      var result = mapper.attr('types');
      expect(result).toEqual('types');
    });
  });

  describe('get() for mapper.parentInstance', function () {
    beforeEach(function () {
      spyOn(CMS.Models, 'get_instance')
        .and.returnValue('parentInstance');
    });

    it('returns parentInstance', function () {
      var result = mapper.attr('parentInstance');
      expect(result).toEqual('parentInstance');
    });
  });

  describe('get() for mapper.useSnapshots', function () {
    it('use Snapshots if using in-scope model', function () {
      var result;
      spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
        .and.returnValue(true);
      result = mapper.attr('useSnapshots');
      expect(result).toEqual(true);
    });

    it('use Snapshots in case Assessment generation',
      function () {
        var result;
        spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
          .and.returnValue(false);
        mapper.attr('assessmentGenerator', true);
        result = mapper.attr('useSnapshots');
        expect(result).toEqual(true);
      });

    it('do not use Snapshots if not an in-scope model ' +
      'and not in assessment generation mode', function () {
      var result;
      spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
        .and.returnValue(false);
      mapper.attr('assessmentGenerator', false);
      result = mapper.attr('useSnapshots');
      expect(result).toEqual(false);
    });
  });

  describe('allowedToCreate() method', function () {
    it('returns true if not in a search mode and is not an in-scope model',
      function () {
        var result;
        mapper.attr('search_only', false);
        spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
          .and.returnValue(false);
        result = mapper.allowedToCreate();
        expect(result).toEqual(true);
      });

    it('returns false if in a search mode and is an in-scope model',
      function () {
        var result;
        mapper.attr('search_only', true);
        spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
          .and.returnValue(true);
        result = mapper.allowedToCreate();
        expect(result).toEqual(false);
      });

    it('returns false if in a search mode and is not an in-scope model',
      function () {
        var result;
        mapper.attr('search_only', true);
        spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
          .and.returnValue(false);
        result = mapper.allowedToCreate();
        expect(result).toEqual(false);
      });

    it('returns false if not in a search mode and is an in-scope model',
      function () {
        var result;
        mapper.attr('search_only', false);
        spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
          .and.returnValue(true);
        result = mapper.allowedToCreate();
        expect(result).toEqual(false);
      });
  });

  describe('showWarning() method', function () {
    it('returns false if is an in-scope model', function () {
      var result;
      spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
        .and.returnValue(true);
      result = mapper.showWarning();
      expect(result).toEqual(false);
    });

    it('returns false if is in assessment generation mode',
      function () {
        var result;
        spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
          .and.returnValue(false);
        mapper.attr('assessmentGenerator', true);
        result = mapper.showWarning();
        expect(result).toEqual(false);
      });

    it('returns false if is in a search mode', function () {
      var result;
      spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
        .and.returnValue(false);
      mapper.attr('search_only', true);
      result = mapper.showWarning();
      expect(result).toEqual(false);
    });

    it('returns true if source object is a Snapshot parent', function () {
      var result;
      spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
        .and.returnValue(false);
      spyOn(GGRC.Utils.Snapshots, 'isSnapshotParent')
        .and.callFake(function (v) {
          return v === 'o';
        });
      mapper.attr('object', 'o');
      mapper.attr('type', 't');
      result = mapper.showWarning();
      expect(result).toEqual(true);
    });

    it('returns true if is mapped object is a ' +
      'Snapshot parent', function () {
      var result;
      spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
        .and.returnValue(false);
      spyOn(GGRC.Utils.Snapshots, 'isSnapshotParent')
        .and.callFake(function (v) {
          return v === 't';
        });
      mapper.attr('object', 'o');
      mapper.attr('type', 't');
      result = mapper.showWarning();
      expect(result).toEqual(true);
    });
  });

  describe('prepareCorrectTypeFormat() method', function () {
    var cmsModel = {
      category: 'category',
      title_plural: 'title_plural',
      model_singular: 'model_singular',
      table_plural: 'table_plural',
      title_singular: 'title_singular'
    };
    var expectedResult = {
      category: 'category',
      name: 'title_plural',
      value: 'model_singular',
      plural: 'title_plural',
      singular: 'model_singular',
      table_plural: 'table_plural',
      title_singular: 'title_singular',
      isSelected: true
    };

    it('returns specified object', function () {
      var result;
      mapper.attr('type', 'model_singular');
      result = mapper.prepareCorrectTypeFormat(cmsModel);
      expect(result).toEqual(expectedResult);
    });

    it('converts models plural title to a snake_case', function () {
      var result;
      var cmsModel1 = Object.assign({}, cmsModel, {
        title_plural: 'Title Plural'
      });
      mapper.attr('type', 'model_singular');
      result = mapper.prepareCorrectTypeFormat(cmsModel1);
      expect(result.plural).toEqual(expectedResult.plural);
    });

    it('is not selected if not equals the mapper type', function () {
      var result;
      mapper.attr('type', 'model_singular_');
      result = mapper.prepareCorrectTypeFormat(cmsModel);
      expect(result.isSelected).toEqual(false);
    });
  });

  describe('addFormattedType() method', function () {
    var groups;
    var type = {
      category: 'category'
    };

    beforeEach(function () {
      groups = {
        governance: {
          items: []
        },
        category: {
          items: []
        }
      };
      spyOn(mapper, 'prepareCorrectTypeFormat')
        .and.returnValue(type);
    });

    it('adds type to governance group if no group with category of this type',
      function () {
        groups.category = undefined;
        spyOn(GGRC.Utils, 'getModelByType')
          .and.returnValue({
            title_singular: 'title_singular'
          });
        mapper.addFormattedType('name', groups);
        expect(groups.governance.items[0]).toEqual(type);
      });

    it('adds type to group of category of this type if this group exist',
      function () {
        groups.governance = undefined;
        spyOn(GGRC.Utils, 'getModelByType')
          .and.returnValue({
            title_singular: 'title_singular'
          });
        mapper.addFormattedType('name', groups);
        expect(groups[type.category].items[0]).toEqual(type);
      });

    it('does nothing if cmsModel is not defined', function () {
      spyOn(GGRC.Utils, 'getModelByType');
      mapper.addFormattedType('name', groups);
      expect(groups.governance.items.length).toEqual(0);
      expect(groups[type.category].items.length).toEqual(0);
    });
    it('does nothing if singular title of cmsModel is not defined',
      function () {
        spyOn(GGRC.Utils, 'getModelByType')
          .and.returnValue({});
        mapper.addFormattedType('name', groups);
        expect(groups.governance.items.length).toEqual(0);
        expect(groups[type.category].items.length).toEqual(0);
      });
    it('does nothing if singular title of cmsModel is "Reference"',
      function () {
        spyOn(GGRC.Utils, 'getModelByType')
          .and.returnValue({
            title_singular: 'Reference'
          });
        mapper.addFormattedType('name', groups);
        expect(groups.governance.items.length).toEqual(0);
        expect(groups[type.category].items.length).toEqual(0);
      });
  });

  describe('getModelNamesList() method', function () {
    var object = 'object';
    var include = ['TaskGroupTask', 'TaskGroup',
      'CycleTaskGroupObjectTask'];
    beforeEach(function () {
      spyOn(GGRC.Mappings, 'getMappingList')
        .and.returnValue('mappingList');
    });

    it('returns names list excluding in-scope snapshots models' +
    ' if it is not search only', function () {
      var result = mapper.getModelNamesList(object);
      expect(result).toEqual('mappingList');
      expect(GGRC.Mappings.getMappingList)
        .toHaveBeenCalledWith(object, [], GGRC.Utils.Snapshots.inScopeModels);
    });

    it('returns names list if it is search only', function () {
      var result;
      mapper.attr('search_only', true);
      result = mapper.getModelNamesList(object);
      expect(result).toEqual('mappingList');
      expect(GGRC.Mappings.getMappingList)
        .toHaveBeenCalledWith(object, include, []);
    });
  });

  describe('initTypes() method', function () {
    var groups = {
      mockData: 123
    };

    beforeEach(function () {
      spyOn(mapper, 'getModelNamesList')
        .and.returnValue([321]);
      spyOn(mapper, 'addFormattedType');
    });

    it('returns groups', function () {
      var result;
      mapper.attr('typeGroups', groups);
      result = mapper.initTypes();
      expect(result).toEqual(groups);
      expect(mapper.addFormattedType)
        .toHaveBeenCalledWith(321, groups);
    });
  });

  describe('setContact() method', function () {
    var contact = {
      email: 'gmail'
    };

    it('sets selected item to contact of mapper', function () {
      mapper.setContact({}, {}, {
        selectedItem: contact
      });
      expect(mapper.attr('contact'))
        .toEqual(jasmine.objectContaining(contact));
    });
  });

  describe('getBindingName() method', function () {
    var instance;

    it('returns binding name with prefix "related_" if instance has no binding',
      function () {
        var result = mapper.getBindingName(instance, 'mock');
        expect(result).toEqual('related_mock');
      });

    it('returns binding name without prefix if instance has binding',
      function () {
        var result;
        instance = {
          has_binding: function () {
            return true;
          }
        };
        result = mapper.getBindingName(instance, 'mock');
        expect(result).toEqual('mock');
      });
  });

  describe('modelFromType() method', function () {
    it('returns undefined if no models', function () {
      var result = mapper.modelFromType('program');
      expect(result).toEqual(undefined);
    });

    it('returns model config by model value', function () {
      var result;
      var types = {
        governance: {
          items: [{
            value: 'v1'
          }, {
            value: 'v2'
          }, {
            value: 'v3'
          }]
        }
      };

      spyOn(mapper, 'initTypes')
        .and.returnValue(types);

      result = mapper.modelFromType('v2');
      expect(result).toEqual(types.governance.items[1]);
    });
  });

  describe('onSubmit() method', function () {
    it('sets true to mapper.afterSearch', function () {
      mapper.attr('afterSearch', false);
      mapper.onSubmit();
      expect(mapper.attr('afterSearch')).toEqual(true);
    });
  });
});

describe('GGRC.Components.modalMapper', function () {
  'use strict';

  var Component;
  var events;
  var scope;
  var handler;
  var helpers;

  beforeAll(function () {
    Component = GGRC.Components.get('modalMapper');
    events = Component.prototype.events;
    helpers = Component.prototype.helpers;
  });
  beforeEach(function () {
    scope = GGRC.Components.getViewModel('modalMapper');
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
        setModel: jasmine.createSpy('setModel'),
        setBinding: jasmine.createSpy('setBinding')
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
    it('calls setBinding()', function () {
      handler.call(that);
      expect(that.setBinding).toHaveBeenCalled();
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
        assessmentTemplate: 'template',
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

    it('sets true to mapper.is_saving and' +
      'returns callback if it is assessment generation', function () {
      var result;
      scope.attr('mapper.assessmentGenerator', true);
      result = handler.call(that, element, event);
      expect(scope.attr('mapper.is_saving')).toEqual(true);
      expect(result).toEqual('expectedResult');
      expect(callback.calls.argsFor(0)[0].length)
        .toEqual(0);
      expect(callback.calls.argsFor(0)[1]).toEqual({
        type: 'type',
        target: 'Program',
        instance: 'instance',
        assessmentTemplate: 'template',
        context: that
      });
    });

    it('calls deferredSave if it is deferred', function () {
      var result;
      scope.attr('deferred', true);
      result = handler.call(that, element, event);
      expect(result).toEqual('deferredSave');
    });
    it('sets false to mapper.is_saving', function () {
      scope.attr('mapper.is_saving', true);
      handler.call(that, element, event);
      expect(scope.attr('mapper.is_saving')).toEqual(false);
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

  describe('"setBinding" handler', function () {
    var selected = {
      has_binding: function () {},
      get_binding: function () {}
    };
    var mapping = {
      instance: {id: 123}
    };
    var binding = {
      refresh_list: function () {}
    };

    beforeEach(function () {
      scope.attr('mapper', {
        getBindingName: function () {},
        parentInstance: selected,
        bindings: []
      });
      selected = scope.attr('mapper.parentInstance');
      handler = events.setBinding;

      spyOn(scope.attr('mapper'), 'getBindingName');
      spyOn(selected, 'get_binding')
        .and.returnValue(binding);
      spyOn(binding, 'refresh_list')
        .and.returnValue($.Deferred().resolve([mapping]));
    });

    it('does nothing if mapper.search_only', function () {
      scope.attr('mapper.search_only', true);
      handler.call({scope: scope});
      expect(scope.attr('mapper').getBindingName)
        .not.toHaveBeenCalled();
    });
    it('does nothing if selected has not binding to tablePlural', function () {
      spyOn(selected, 'has_binding')
        .and.returnValue(false);
      handler.call({scope: scope});
      expect(scope.attr('mapper').getBindingName)
        .toHaveBeenCalled();
      expect(selected.get_binding)
        .not.toHaveBeenCalled();
    });
    it('adds mappings to mapper.bindings', function () {
      spyOn(selected, 'has_binding')
        .and.returnValue(true);
      handler.call({scope: scope});
      expect(scope.attr('mapper.bindings')[123]).toEqual(mapping);
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
        assessmentGenerator: true,
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
    it('calls setBinding()', function () {
      handler.call(that);
      expect(that.setBinding).toHaveBeenCalled();
    });
    it('sets empty array to mapper.relevant if it is assessment generation',
      function () {
        scope.attr('mapper.assessmentGenerator', false);
        spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
          .and.returnValue(false);
        handler.call(that);
        expect(scope.attr('mapper.relevant').length)
          .toEqual(0);
      });
  });

  describe('"{mapper} assessmentTemplate" handler', function () {
    beforeEach(function () {
      scope.attr('mapper', {

      });
      handler = events['{mapper} assessmentTemplate'];
    });

    it('sets false to mapper.block_type_change if value is empty',
      function () {
        handler.call({scope: scope});
        expect(scope.attr('mapper.block_type_change'))
          .toEqual(false);
      });
    it('sets true to mapper.block_type_change if value is not empty',
      function () {
        handler.call({scope: scope}, scope, {}, 'mock-value');
        expect(scope.attr('mapper.block_type_change'))
          .toEqual(true);
      });
    it('sets type to mapper.type if value is not empty',
      function () {
        handler.call({scope: scope}, scope, {}, 'mock-value');
        expect(scope.attr('mapper.type'))
          .toEqual('value');
      });
  });

  describe('"#search-by-owner autocomplete:select" handler', function () {
    beforeEach(function () {
      scope.attr('mapper', {});
      handler = events['#search-by-owner autocomplete:select'];
    });

    it('sets data to mapper.contact', function () {
      handler.call({scope: scope}, {}, {}, {item: 'mock'});
      expect(scope.attr('mapper.contact')).toEqual('mock');
    });
  });

  describe('"#search-by-owner keyup" handler', function () {
    var element;
    beforeEach(function () {
      scope.attr('mapper', {
        contact: 123
      });
      element = $('<input type="text"/>');
      handler = events['#search-by-owner keyup'];
    });

    it('does nothing if value of element is empty', function () {
      handler.call({scope: scope}, element);
      expect(scope.attr('mapper.contact'))
        .toEqual(jasmine.objectContaining({}));
    });
    it('does nothing if value of element is not empty', function () {
      element.val(321);
      handler.call({scope: scope}, element);
      expect(scope.attr('mapper.contact')).toEqual(123);
    });
  });

  describe('"#search keyup" handler', function () {
    var element;
    var spyObj = {
      setItems: function () {}
    };
    var mapperResults = {
      find: function () {
        return {
          scope: function () {
            return spyObj;
          }
        };
      }
    };

    beforeEach(function () {
      scope.attr('mapper', {
        filter: 123
      });
      element = $('<input type="text"/>');
      handler = events['#search keyup'];
      spyOn(spyObj, 'setItems');
    });

    it('does nothing if keyCode of event is not 13', function () {
      handler.call({scope: scope}, element, {keyCode: 32});
      expect(scope.attr('mapper.filter'))
        .toEqual(123);
    });
    it('sets value of element to mapper-results if keyCode of event is 13',
      function () {
        element.val(321);
        handler.call({
          scope: scope,
          element: mapperResults
        }, element, {keyCode: 13});
        expect(scope.attr('mapper.filter')).toEqual('321');
      });
    it('calls setItems of mapper-results.scope if keyCode of event is 13',
      function () {
        element.val(321);
        handler.call({
          scope: scope,
          element: mapperResults
        }, element, {keyCode: 13});
        expect(spyObj.setItems).toHaveBeenCalled();
      });
  });

  describe('"allSelected" handler', function () {
    beforeEach(function () {
      scope.attr('mapper', {
        selected: [],
        entries: [],
        all_selected: 'mock'
      });
      handler = events.allSelected;
    });

    it('does not change mapper.allSelected' +
    'if length of entries and selected is 0', function () {
      handler.call({scope: scope});
      expect(scope.attr('mapper.all_selected')).toEqual('mock');
    });
    it('does nothing if length of entries and selected is 0', function () {
      scope.attr('mapper.selected', [1, 2]);
      scope.attr('mapper.entries', [1, 2]);
      handler.call({scope: scope});
      expect(scope.attr('mapper.all_selected')).toEqual(true);
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

  describe('loading_or_saving() helper', function () {
    var helper;
    var options = {
      fn: function () {
        return 'fn';
      },
      inverse: function () {
        return 'inverse';
      }
    };

    beforeEach(function () {
      helper = helpers.loading_or_saving;
    });

    it('returns options.fn() if it is page loading', function () {
      var result;
      scope.attr('mapper', {
        page_loading: true
      });
      result = helper.call(scope, options);
      expect(result).toEqual('fn');
    });
    it('returns options.fn() if it is saving', function () {
      var result;
      scope.attr('mapper', {
        is_saving: true
      });
      result = helper.call(scope, options);
      expect(result).toEqual('fn');
    });
    it('returns options.fn() if it is block type changing',
      function () {
        var result;
        scope.attr('mapper', {
          block_type_change: true
        });
        result = helper.call(scope, options);
        expect(result).toEqual('fn');
      });
    it('returns options.inverse() if it is not page loading,' +
    'not saving and not block type changing', function () {
      var result;
      scope.attr('mapper', {});
      result = helper.call(scope, options);
      expect(result).toEqual('inverse');
    });
  });
});
