/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Component.ReadMore', function () {
  'use strict';
  var vm;

  beforeEach(function () {
    vm = GGRC.Components.getViewModel('readMore');
  });

  describe('toggle() method', function () {
    var eventMock;

    beforeEach(function () {
      eventMock = {
        stopPropagation: jasmine.createSpy()
      };
    });

    it('calls stopPropagation()', function () {
      vm.toggle(eventMock);

      expect(eventMock.stopPropagation).toHaveBeenCalled();
    });

    it('switchs expanded attribute', function () {
      vm.attr('expanded', true);
      vm.toggle(eventMock);

      expect(vm.attr('expanded')).toBe(false);
      vm.toggle(eventMock);

      expect(vm.attr('expanded')).toBe(true);
    });
  });
  describe('set() of cssClass attribute', function () {
    it('returns empty string if viewModel.expanded is true', function () {
      vm.attr('expanded', true);
      expect(vm.attr('cssClass')).toEqual('');
    });
    it('returns specific css string ' +
    'if viewModel.expanded is false', function () {
      var i = 1;
      for (; i <= 10; i++) {
        vm.attr('maxLinesNumber', i);
        expect(vm.attr('cssClass')).toEqual('ellipsis-truncation-' + i);
      }
    });
  });
  describe('isOverflowing(element) method', function () {
    var element;

    describe('if component is not expanded', function () {
      it('sets true to overflowing' +
      ' if scrollHeight of element greater then clientHeight', function () {
        vm.attr('expanded', false);
        element = {
          scrollHeight: 100,
          clientHeight: 50
        };
        vm.isOverflowing(element);
        expect(vm.attr('overflowing')).toBe(true);
      });
      it('sets false to overflowing if scrollHeight' +
      ' of element less or equal then clientHeight', function () {
        vm.attr('expanded', false);
        element = {
          scrollHeight: 100,
          clientHeight: 101
        };
        vm.isOverflowing(element);
        expect(vm.attr('overflowing')).toBe(false);
      });
    });

    describe('if component is expanded', function () {
      it('sets true to overflowing if clientHeight of element' +
      ' greater or equal then minimal allowed height', function () {
        vm.attr('expanded', true);
        vm.attr('lineHeight', 20);
        vm.attr('maxLinesNumber', 5);
        element = {
          clientHeight: 100
        };
        vm.isOverflowing(element);
        expect(vm.attr('overflowing')).toBe(true);
      });
      it('sets false to overflowing if clientHeight of element' +
      ' less then minimal allowed height', function () {
        vm.attr('expanded', true);
        vm.attr('lineHeight', 20);
        vm.attr('maxLinesNumber', 5);
        element = {
          clientHeight: 80
        };
        vm.isOverflowing(element);
        expect(vm.attr('overflowing')).toBe(false);
      });
    });
  });
});
