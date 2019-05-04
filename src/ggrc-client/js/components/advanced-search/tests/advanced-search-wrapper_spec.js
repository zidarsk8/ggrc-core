/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../advanced-search-wrapper';
import * as AdvancedSearch from '../../../plugins/utils/advanced-search-utils';
import * as StateUtils from '../../../plugins/utils/state-utils';

describe('advanced-search-wrapper component', function () {
  'use strict';

  let viewModel;
  let events;
  let spy;
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

  describe('setDefaultStatusItem method', () => {
    it('should call setDefaultStatusConfig if hasStatusFilter', () => {
      spyOn(StateUtils, 'hasFilter').and.returnValue(true);
      spy = spyOn(AdvancedSearch, 'setDefaultStatusConfig');

      viewModel.setDefaultStatusItem();
      expect(spy).toHaveBeenCalled();
    });

    it('should call create.state if !hasStatusFilter', () => {
      spyOn(StateUtils, 'hasFilter').and.returnValue(false);
      spy = spyOn(AdvancedSearch.create, 'state');

      viewModel.setDefaultStatusItem();
      expect(spy).toHaveBeenCalled();
    });
  });
});
