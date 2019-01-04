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

    it('should subscribe on router widget change', () => {
      spyOn(router, 'bind');

      init();
      expect(router.bind).toHaveBeenCalledWith('widget', jasmine.any(Function));
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
    });
  });
});
