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

  describe('events', () => {
    let events;
    let handler;

    beforeEach(() => {
      events = Component.prototype.events;
    });

    describe('"inserted" handler', () => {
      beforeEach(() => {
        handler = events.inserted.bind({viewModel: vm});
      });

      describe('if RELEASE_NOTES_DATE not equal to saved date', () => {
        beforeEach(() => {
          spyOn(localStorage, 'getItem')
            .and.returnValue(new Date());
          spyOn(localStorage, 'setItem');
          spyOn(vm, 'open');
        });

        it('sets RELEASE_NOTES_DATE into localStorage as GGRC.RELEASE_NOTES_DATE', () => {
          handler();

          expect(localStorage.setItem)
            .toHaveBeenCalledWith('GGRC.RELEASE_NOTES_DATE', RELEASE_NOTES_DATE);
        });

        it('calls open() method', () => {
          handler();

          expect(vm.open).toHaveBeenCalled();
        });
      });

      describe('if RELEASE_NOTES_DATE equal to saved date', () => {
        beforeEach(() => {
          spyOn(localStorage, 'getItem')
            .and.returnValue(RELEASE_NOTES_DATE);
          spyOn(localStorage, 'setItem');
          spyOn(vm, 'open');
        });

        it('does not change date in localStorage', () => {
          handler();

          expect(localStorage.setItem).not.toHaveBeenCalledWith(
            'GGRC.RELEASE_NOTES_DATE', RELEASE_NOTES_DATE);
        });

        it('does not call open() method', () => {
          handler();

          expect(vm.open).not.toHaveBeenCalled();
        });
      });
    });
  });
});
