/* !
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  */

describe('GGRC.Components.subTreeModels', function () {
  var vm;
  var events;

  beforeEach(function () {
    vm = GGRC.Components.getViewModel('subTreeModels');
    events = GGRC.Components.get('subTreeModels').prototype.events;
  });

  describe('get() of uniqueModelsList', function () {
    it('sets random stringified number to inputIdPrefix', function () {
      var result;
      vm.attr('modelsList', new can.List([
        {}, {}, {}, {}, {},
      ]));

      result = _.uniq(vm.attr('uniqueModelsList'), function (el) {
        return el.attr('inputId');
      });

      expect(result.length).toEqual(5);
    });
  });

  describe('activate() method', function () {
    it('sets true to viewModel.isActive', function () {
      vm.attr('isActive', false);

      vm.activate();
      expect(vm.attr('isActive')).toBe(true);
    });
  });

  describe('setDisplayModels() method', function () {
    var event;
    var modelsList;

    beforeEach(function () {
      modelsList = new can.List([
        {name: 'Audit', display: true},
        {name: 'Control', display: true},
        {name: 'Objective', display: false},
        {name: 'Market', display: true},
      ]);
      spyOn(can, 'trigger');
      event = {
        stopPropagation: jasmine.createSpy(),
      };
      vm.attr('modelsList', modelsList);
      vm.attr('$el', 'element');
    });

    it('triggers event "childModelsChange" on element' +
    ' with array of selected models', function () {
      var selectedModels;

      vm.setDisplayModels(event);
      selectedModels = modelsList.filter(function (item) {
        return item.display;
      }).map(function (item) {
        return item.name;
      }).serialize();

      expect(can.trigger).toHaveBeenCalledWith(vm.attr('$el'),
        'childModelsChange', [jasmine.objectContaining(selectedModels)]);
    });

    it('sets false to viewModel.isActive', function () {
      vm.attr('isActive', true);

      vm.setDisplayModels(event);
      expect(vm.attr('isActive')).toBe(false);
    });
  });

  describe('selectAll(), selectNone() methods', function () {
    var modelsList;
    var event;

    beforeEach(function () {
      modelsList = new can.List([
        {name: 'Audit', display: true},
        {name: 'Control', display: true},
        {name: 'Objective', display: false},
        {name: 'Market', display: true},
      ]);
      vm.attr('modelsList', modelsList);
      event = {
        stopPropagation: jasmine.createSpy(),
      };
    });

    it('selectAll() sets display true to all models in list', function () {
      var result;

      vm.selectAll(event);
      result = _.every(vm.attr('modelsList'), function (item) {
        return item.display === true;
      });
      expect(result).toBe(true);
    });

    it('selectNone() sets display false to all models in list', function () {
      var result;

      vm.selectNone(event);
      result = _.every(vm.attr('modelsList'), function (item) {
        return item.display === false;
      });
      expect(result).toBe(true);
    });
  });

  describe('inserted handler', function () {
    var handler;
    var viewModel;

    beforeEach(function () {
      viewModel = new can.Map({});
      handler = events['inserted'].bind({
        viewModel: viewModel,
        element: 'element',
      });
    });

    it('saves element into viewModel', function () {
      handler();
      expect(viewModel.attr('$el')).toEqual('element');
    });
  });

  describe('".sub-tree-models mouseleave" handler', function () {
    var handler;
    var viewModel;

    beforeEach(function () {
      viewModel = new can.Map();
      handler = events['.sub-tree-models mouseleave'].bind({
        viewModel: viewModel,
      });
    });

    it('sets false to viewModel.isActive', function () {
      viewModel.attr('isActive', true);

      handler();
      expect(viewModel.attr('isActive', false));
    });
  });
});
