/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
import Component from '../inner-nav';
import {getComponentVM} from '../../../../js_specs/spec_helpers';
import router, * as RouterUtils from '../../../router';
import * as ObjectVersionsUtils
  from '../../../plugins/utils/object-versions-utils';

describe('inner-nav component', () => {
  let viewModel;

  beforeEach(() => {
    viewModel = getComponentVM(Component);
  });

  describe('init() method', () => {
    let init;
    beforeEach(() => {
      init = Component.prototype.init.bind({
        viewModel,
      });
    });

    it('should call handleDescriptors()', () => {
      spyOn(viewModel, 'handleDescriptors');
      init();

      expect(viewModel.handleDescriptors).toHaveBeenCalled();
    });
  });

  describe('viewModel', () => {
    describe('handleDescriptors() method', () => {
      it('should create widgets from descriptors', () => {
        spyOn(viewModel, 'createWidget').and.returnValue({});
        viewModel.attr('widgetList', null);

        let descriptors = [{}, {}, {}];
        viewModel.attr('widgetDescriptors', descriptors);

        viewModel.handleDescriptors();

        expect(viewModel.createWidget).toHaveBeenCalledTimes(3);
        expect(viewModel.attr('widgetList').length).toBe(3);
      });

      it('should sort widgets by order and title', () => {
        let descriptors = [
          {order: 3, widget_name: 'b'},
          {order: 2, widget_name: 'a'},
          {order: 3, widget_name: 'a'},
          {order: 2, widget_name: 'b'},
        ];
        viewModel.attr('widgetDescriptors', descriptors);

        viewModel.handleDescriptors();

        let widgets = viewModel.attr('widgetList');

        expect(widgets[0])
          .toEqual(jasmine.objectContaining({order: 2, title: 'a'}));
        expect(widgets[1])
          .toEqual(jasmine.objectContaining({order: 2, title: 'b'}));
        expect(widgets[2])
          .toEqual(jasmine.objectContaining({order: 3, title: 'a'}));
        expect(widgets[3])
          .toEqual(jasmine.objectContaining({order: 3, title: 'b'}));
      });
    });

    describe('createWidget() method', () => {
      it('should set id', () => {
        let result = viewModel.createWidget({widget_id: 'id'});
        expect(result.id).toBe('id');
      });

      it('should set title when widgetName is function in descriptor', () => {
        let result = viewModel.createWidget({
          widget_name: () => 'title',
        });
        expect(result.title).toBe('title');
      });

      it('should set title when widgetName is string in descriptor', () => {
        let result = viewModel.createWidget({
          widget_name: 'title',
        });
        expect(result.title).toBe('title');
      });

      it('should set empty type for not object version widgets', () => {
        spyOn(ObjectVersionsUtils, 'isObjectVersion').and.returnValue(false);
        let result = viewModel.createWidget({widget_id: 'id'});
        expect(result.type).toBe('');
      });

      it('shoult set version type for object versions widgets', () => {
        spyOn(ObjectVersionsUtils, 'isObjectVersion').and.returnValue(true);
        let result = viewModel.createWidget({widget_id: 'id'});
        expect(result.type).toBe('version');
      });

      it('should set icon', () => {
        let result = viewModel.createWidget({widget_icon: 'icon'});
        expect(result.icon).toBe('icon');
      });

      it('should set href', () => {
        spyOn(RouterUtils, 'buildUrl').and.returnValue('href');
        let result = viewModel.createWidget({widget_id: 'id'});
        expect(result.href).toBe('href');
      });

      it('should set model', () => {
        let result = viewModel.createWidget({model: 'model'});
        expect(result.model).toBe('model');
      });

      it('should set order', () => {
        let result = viewModel.createWidget({order: 'order'});
        expect(result.order).toBe('order');
      });

      it('should set uncountable', () => {
        let result = viewModel.createWidget({uncountable: true});
        expect(result.uncountable).toBe(true);
      });

      it('should set forceRefetch', () => {
        let result = viewModel.createWidget({forceRefetch: true});
        expect(result.forceRefetch).toBe(true);
      });
    });

    describe('route(widgetId) method', () => {
      it('should find widget in widgetList', () => {
        spyOn(viewModel, 'findWidget');

        viewModel.route('widget id');

        expect(viewModel.findWidget).toHaveBeenCalledWith('widget id');
      });

      it('should select first widget from widgetList '
        + 'if selected widget is not in the list', () => {
        spyOn(viewModel, 'findWidget').and.returnValue(null);
        viewModel.attr('widgetList', [{id: '1'}, {id: '2'}]);
        spyOn(router, 'attr');

        viewModel.route('selected widget id');
        expect(router.attr).toHaveBeenCalledWith('widget', '1');
      });

      it('should set activeWidget if widget is in widgetList ', () => {
        let widget = {id: '1'};
        spyOn(viewModel, 'findWidget').and.returnValue(widget);
        viewModel.attr('activeWidget', null);

        viewModel.route('1');

        expect(viewModel.attr('activeWidget').serialize()).toEqual(widget);
      });

      it('should dispatch "activeChanged" event if widget is in widgetList',
        () => {
          spyOn(viewModel, 'dispatch');
          let widget = {id: '1'};
          spyOn(viewModel, 'findWidget').and.returnValue(widget);

          viewModel.route('1');

          expect(viewModel.dispatch).toHaveBeenCalledWith({
            type: 'activeChanged',
            widget,
          });
        });
    });

    describe('findWidget(widgetId) method', () => {
      it('should search widgets by id in widgetList', () => {
        let widget1 = {id: '1'};
        let widget2 = {id: '2'};
        viewModel.attr('widgetList', [widget1, widget2]);

        let result = viewModel.findWidget('2');

        expect(result.serialize()).toEqual(widget2);
      });

      it('retuns undefined when widget is not found', () => {
        let widget1 = {id: '1'};
        let widget2 = {id: '2'};
        viewModel.attr('widgetList', [widget1, widget2]);

        let result = viewModel.findWidget('3');

        expect(result).toBeUndefined();
      });
    });
  });

  describe('events', () => {
    describe('inserted event', () => {
      let event;
      beforeEach(() => {
        event = Component.prototype.events['inserted'].bind({viewModel});
      });

      it('should subscribe on router widget change', () => {
        spyOn(router, 'bind');

        event();
        expect(router.bind)
          .toHaveBeenCalledWith('widget', jasmine.any(Function));
      });

      it('should route to selected in router widget', () => {
        spyOn(viewModel, 'route');
        router.attr('widget', 'selected widget');
        event();

        expect(viewModel.route).toHaveBeenCalledWith('selected widget');
      });
    });
  });
});
