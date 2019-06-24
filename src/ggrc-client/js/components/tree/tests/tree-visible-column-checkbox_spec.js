/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../tree-visible-column-checkbox';
import {getComponentVM} from '../../../../js_specs/spec_helpers';

describe('tree-visible-column-checkbox', () => {
  let viewModel;

  beforeEach(() => {
    viewModel = getComponentVM(Component);
  });

  describe('getTitle method', () => {
    it("returns title when it's string", () => {
      const item = {title: 'cool test title', name: 'some name'};
      expect(viewModel.getTitle(item)).toBe('cool test title');
    });

    it("calls title with viewType when it's function and returns "+
        'this function return value', () => {
      const item = {title: () => {}, name: 'some name'};
      spyOn(item, 'title').and.returnValue('really nice title');
      expect(viewModel.getTitle(item)).toBe('really nice title');
      expect(item.title).toHaveBeenCalled();
    });
  });
});
