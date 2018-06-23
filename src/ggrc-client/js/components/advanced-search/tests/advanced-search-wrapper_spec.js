/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../advanced-search-wrapper';

describe('advanced-search-wrapper component', function () {
  'use strict';

  let viewModel;
  let events;
  beforeEach(() => {
    viewModel = getComponentVM(Component);
    events = Component.prototype.events;
  });

  describe('"{viewModel} modelName" handler', function () {
    let that;
    let handler;
    beforeEach(function () {
      that = {
        viewModel: viewModel,
      };
      handler = events['{viewModel} modelName'];
    });

    it('calls resetFilters() method', function () {
      spyOn(viewModel, 'resetFilters');
      handler.call(that);
      expect(viewModel.resetFilters).toHaveBeenCalled();
    });
  });
});
