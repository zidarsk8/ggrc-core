/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Component from '../read-more';

describe('GGRC.Component.ReadMore', () => {
  let vm;
  beforeEach(() => {
    vm = new (can.Map.extend(Component.prototype.viewModel));
  });

  describe('toggle() method', () => {
    let eventMock;

    beforeEach(() => {
      eventMock = {
        stopPropagation: jasmine.createSpy(),
      };
    });

    it('calls stopPropagation()', () => {
      vm.toggle(eventMock);

      expect(eventMock.stopPropagation).toHaveBeenCalled();
    });

    it('switchs expanded attribute', () => {
      vm.attr('expanded', true);
      vm.toggle(eventMock);

      expect(vm.attr('expanded')).toBe(false);
      vm.toggle(eventMock);

      expect(vm.attr('expanded')).toBe(true);
    });
  });
  describe('set() of cssClass attribute', () => {
    it('returns empty string if viewModel.expanded is true', () => {
      vm.attr('expanded', true);
      expect(vm.attr('cssClass')).toEqual('');
    });
    it('returns specific css string ' +
    'if viewModel.expanded is false', () => {
      for (let i; i <= 10; i++) {
        vm.attr('maxLinesNumber', i);
        expect(vm.attr('cssClass')).toEqual('ellipsis-truncation-' + i);
      }
    });
  });
  describe('isOverflowing(element) method', () => {
    let element;

    describe('if component is not expanded', () => {
      it('sets true to overflowing' +
      ' if scrollHeight of element greater then clientHeight', () => {
        vm.attr('expanded', false);
        element = {
          scrollHeight: 100,
          clientHeight: 50,
        };
        vm.isOverflowing(element);
        expect(vm.attr('overflowing')).toBe(true);
      });
      it('sets false to overflowing if scrollHeight' +
      ' of element less or equal then clientHeight', () => {
        vm.attr('expanded', false);
        element = {
          scrollHeight: 100,
          clientHeight: 101,
        };
        vm.isOverflowing(element);
        expect(vm.attr('overflowing')).toBe(false);
      });
    });

    describe('if component is expanded', () => {
      it('sets true to overflowing if clientHeight of element' +
      ' greater or equal then minimal allowed height', () => {
        vm.attr('expanded', true);
        vm.attr('lineHeight', 20);
        vm.attr('maxLinesNumber', 5);
        element = {
          clientHeight: 100,
        };
        vm.isOverflowing(element);
        expect(vm.attr('overflowing')).toBe(true);
      });
      it('sets false to overflowing if clientHeight of element' +
      ' less then minimal allowed height', () => {
        vm.attr('expanded', true);
        vm.attr('lineHeight', 20);
        vm.attr('maxLinesNumber', 5);
        element = {
          clientHeight: 80,
        };
        vm.isOverflowing(element);
        expect(vm.attr('overflowing')).toBe(false);
      });
    });
  });
});
