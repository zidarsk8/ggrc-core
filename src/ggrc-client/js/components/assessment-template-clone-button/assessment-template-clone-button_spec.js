/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from './assessment-template-clone-button';
import {getComponentVM} from '../../../js_specs/spec_helpers';
import router from '../../router';

describe('assessment-template-clone-button component', () => {
  let vm;

  beforeEach(() => {
    vm = getComponentVM(Component);
  });

  describe('refreshTreeView() method', () => {
    let pageInstanceSpy;
    let routerSpy;

    beforeEach(() => {
      spyOn(vm, 'dispatch');
      routerSpy = spyOn(router, 'attr');
      pageInstanceSpy = spyOn(GGRC, 'page_instance');
    });

    it('dispatches "refreshTree" if it is Audit page ' +
    'and assessment_template widget', () => {
      pageInstanceSpy.and.returnValue({type: 'Audit'});
      routerSpy.and.returnValue('assessment_template_widget');

      vm.refreshTreeView();

      expect(vm.dispatch).toHaveBeenCalledWith('refreshTree');
    });

    it('sets "assessment_template_widget" to router with refetch flag ' +
    'if it is Audit page but not assessment_template widget', () => {
      pageInstanceSpy.and.returnValue({type: 'Audit'});

      vm.refreshTreeView();

      expect(router.attr).toHaveBeenCalledWith({
        widget: 'assessment_template_widget',
        refetch: true,
      });
    });

    it('sets "assessment_template_widget" to router with refetch flag ' +
    'if it is Audit page but not assessment_template widget', () => {
      pageInstanceSpy.and.returnValue({type: 'People'});

      vm.refreshTreeView();

      expect(router.attr).not.toHaveBeenCalledWith({
        widget: 'assessment_template_widget',
        refetch: true,
      });
      expect(vm.dispatch).not.toHaveBeenCalledWith('refreshTree');
    });
  });
});
