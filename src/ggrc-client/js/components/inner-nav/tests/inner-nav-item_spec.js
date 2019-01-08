/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
import Component from '../inner-nav-item';
import {getComponentVM} from '../../../../js_specs/spec_helpers';

describe('inner-nav-item component', () => {
  let viewModel;

  beforeEach(() => {
    viewModel = getComponentVM(Component);
  });

  describe('displayTab property', () => {
    it('should return TRUE when widget has count', () => {
      let widget = {
        hasCount: true,
        count: 5,
        uncountable: false,
        title: 'widget',
        forceShow: false,
        inForceShowList: false,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', false);

      let result = viewModel.attr('displayTab');
      expect(result).toBeTruthy();
    });

    it('should return TRUE when widget is uncountable', () => {
      let widget = {
        hasCount: false,
        count: 0,
        uncountable: true,
        title: 'widget',
        forceShow: false,
        inForceShowList: false,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', false);

      let result = viewModel.attr('displayTab');
      expect(result).toBeTruthy();
    });

    it('should return TRUE when forceShow is true', () => {
      let widget = {
        hasCount: false,
        count: 0,
        uncountable: false,
        title: 'widget',
        forceShow: true,
        inForceShowList: false,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', false);

      let result = viewModel.attr('displayTab');
      expect(result).toBeTruthy();
    });

    it('should return TRUE when all tabs should be shown', () => {
      let widget = {
        hasCount: false,
        count: 0,
        uncountable: false,
        title: 'widget',
        forceShow: false,
        inForceShowList: false,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', true);

      let result = viewModel.attr('displayTab');
      expect(result).toBeTruthy();
    });

    it('should return TRUE when widget in forceShowList', () => {
      let widget = {
        hasCount: false,
        count: 0,
        uncountable: false,
        title: 'widget',
        forceShow: false,
        inForceShowList: true,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', false);

      let result = viewModel.attr('displayTab');
      expect(result).toBeTruthy();
    });

    it('should return FALSE when widget should not be displayed', () => {
      let widget = {
        hasCount: false,
        count: 0,
        uncountable: false,
        title: 'widget',
        forceShow: false,
        inForceShowList: false,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', false);

      let result = viewModel.attr('displayTab');
      expect(result).toBeFalsy();
    });
  });

  describe('showCloseButton property', () => {
    it('should return FALSE when hasCount is false', () => {
      let widget = {
        hasCount: false,
        count: 5,
        title: 'widget',
        inForceShowList: false,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', false);

      let result = viewModel.attr('showCloseButton');
      expect(result).toBeFalsy();
    });

    it('should return FALSE when widget count is not 0', () => {
      let widget = {
        hasCount: true,
        count: 5,
        title: 'widget',
        inForceShowList: false,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', false);

      let result = viewModel.attr('showCloseButton');
      expect(result).toBeFalsy();
    });

    it('should return FALSE when all tabs should be shown', () => {
      let widget = {
        hasCount: true,
        count: 0,
        title: 'widget',
        inForceShowList: false,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', true);

      let result = viewModel.attr('showCloseButton');
      expect(result).toBeFalsy();
    });

    it('should return FALSE when widget in forceShowList', () => {
      let widget = {
        hasCount: true,
        count: 0,
        title: 'widget',
        inForceShowList: true,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', false);

      let result = viewModel.attr('showCloseButton');
      expect(result).toBeFalsy();
    });

    it('should return TRUE when tab can be closed', () => {
      let widget = {
        hasCount: true,
        count: 0,
        title: 'widget',
        inForceShowList: false,
      };
      viewModel.attr('widget', widget);
      viewModel.attr('showAllTabs', false);

      let result = viewModel.attr('showCloseButton');
      expect(result).toBeTruthy();
    });
  });

  describe('closeTab() method', () => {
    it('should dispatch close event', () => {
      spyOn(viewModel, 'dispatch');
      let widget = new can.Map();
      viewModel.attr('widget', widget);

      viewModel.closeTab();

      expect(viewModel.dispatch).toHaveBeenCalledWith({
        type: 'close',
        widget,
      });
    });

    it('should return FALSE to stop event propagation', () => {
      let result = viewModel.closeTab();

      expect(result).toBeFalsy();
    });
  });
});
