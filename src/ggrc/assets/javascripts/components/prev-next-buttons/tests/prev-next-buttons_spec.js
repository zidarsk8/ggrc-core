/*!
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.prevNextButtons', function () {
  'use strict';

  describe('hasNext getter', function () {
    var viewModel;

    beforeAll(function () {
      viewModel = GGRC.Components.getViewModel('prevNextButtons');
    });

    it('returns true when current index is less than total',
      function () {
        var result;
        viewModel.attr('currentIndex', 1);
        viewModel.attr('totalCount', 3);

        result = viewModel.attr('hasNext');

        expect(result).toBeTruthy();
      });

    it('returns false when current index is greater than total',
      function () {
        var result;
        viewModel.attr('currentIndex', 4);
        viewModel.attr('totalCount', 3);

        result = viewModel.attr('hasNext');

        expect(result).toBeFalsy();
      });

    it('returns false when current index is equal to last item number',
      function () {
        var result;
        viewModel.attr('currentIndex', 2);
        viewModel.attr('totalCount', 3);

        result = viewModel.attr('hasNext');

        expect(result).toBeFalsy();
      });

    it('returns false when current index is equal to total',
      function () {
        var result;
        viewModel.attr('currentIndex', 3);
        viewModel.attr('totalCount', 3);

        result = viewModel.attr('hasNext');

        expect(result).toBeFalsy();
      });
  });

  describe('hasPrev getter', function () {
    var viewModel;

    beforeAll(function () {
      viewModel = GGRC.Components.getViewModel('prevNextButtons');
    });

    it('returns true when current index is greater than 0',
      function () {
        var result;
        viewModel.attr('currentIndex', 1);

        result = viewModel.attr('hasPrev');

        expect(result).toBeTruthy();
      });

    it('returns false when current index equals 0',
      function () {
        var result;
        viewModel.attr('currentIndex', 0);

        result = viewModel.attr('hasPrev');

        expect(result).toBeFalsy();
      });
  });

  describe('setNext method', function () {
    var viewModel;

    beforeAll(function () {
      viewModel = GGRC.Components.getViewModel('prevNextButtons');
    });

    it('increments current index when there is next item',
      function () {
        var result;
        viewModel.attr('currentIndex', 1);
        viewModel.attr('totalCount', 3);

        viewModel.setNext();
        result = viewModel.attr('currentIndex');

        expect(result).toEqual(2);
      });

    it('leaves current index as is when it is last item',
      function () {
        var result;
        viewModel.attr('currentIndex', 2);
        viewModel.attr('totalCount', 3);

        viewModel.setNext();
        result = viewModel.attr('currentIndex');

        expect(result).toEqual(2);
      });

    it('leaves current index as is when there is no next item',
      function () {
        var result;
        viewModel.attr('currentIndex', 3);
        viewModel.attr('totalCount', 3);

        viewModel.setNext();
        result = viewModel.attr('currentIndex');

        expect(result).toEqual(3);
      });
  });

  describe('setPrev method', function () {
    var viewModel;

    beforeAll(function () {
      viewModel = GGRC.Components.getViewModel('prevNextButtons');
    });

    it('decrements current index when there is previous item',
      function () {
        var result;
        viewModel.attr('currentIndex', 1);

        viewModel.setPrev();
        result = viewModel.attr('currentIndex');

        expect(result).toEqual(0);
      });

    it('leaves current index as is when there is no previous item',
      function () {
        var result;
        viewModel.attr('currentIndex', 0);

        viewModel.setPrev();
        result = viewModel.attr('currentIndex');

        expect(result).toEqual(0);
      });
  });
});
