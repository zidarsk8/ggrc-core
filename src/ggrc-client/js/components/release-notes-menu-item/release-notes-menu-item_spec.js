/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from './release-notes-menu-item';
import {getComponentVM} from '../../../js_specs/spec_helpers';

describe('"release-notes-menu-item" component', () => {
  let vm;

  beforeEach(() => {
    vm = getComponentVM(Component);
  });

  describe('open() method', () => {
    it('sets true to "state.open" flag', () => {
      vm.attr('state.open', false);

      vm.open();

      expect(vm.attr('state.open')).toBe(true);
    });
  });
});
