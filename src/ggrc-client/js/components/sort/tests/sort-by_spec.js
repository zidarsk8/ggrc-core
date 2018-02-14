/*
 Copyright (C) 2018 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../sort-by';

describe('sort-by component', () => {
  let viewModel;

  beforeAll(()=> {
    viewModel = getComponentVM(Component);
  });

  describe('"sort()" method', () => {
    const testItems = [
      {title: 'B'},
      {title: 'C'},
      {title: 'A'},
    ];

    it('should sort items by title and call "getModels" method', (done) => {
      const promise = new Promise((resolve, reject) => {
        resolve(testItems);
      });

      spyOn(viewModel, 'getModels').and.returnValue(promise);

      viewModel.attr('items', testItems);
      viewModel.attr('sortByProperty', 'title');
      viewModel.sort();

      promise.then((data) => {
        const sortedItems = viewModel.attr('sortedItems');
        expect(sortedItems.length).toBe(3);
        expect(sortedItems[0].title).toEqual('A');
        expect(sortedItems[1].title).toEqual('B');
        expect(sortedItems[2].title).toEqual('C');

        expect(viewModel.getModels).toHaveBeenCalled();
        done();
      });
    });

    it('should sort items by title. snapshot instance', () => {
      let sortedItems;

      viewModel.attr('items', testItems);
      viewModel.attr('isSnapshot', true);
      viewModel.attr('sortByProperty', 'title');
      viewModel.sort();

      sortedItems = viewModel.attr('sortedItems');
      expect(sortedItems.length).toBe(3);
      expect(sortedItems[0].title).toEqual('A');
      expect(sortedItems[1].title).toEqual('B');
      expect(sortedItems[2].title).toEqual('C');
    });

    it('should not sort items. "sortByProperty" is not set', () => {
      let sortedItems;

      viewModel.attr('items', testItems);
      viewModel.attr('isSnapshot', true);
      viewModel.attr('sortByProperty', '');
      viewModel.sort();

      sortedItems = viewModel.attr('sortedItems');
      expect(sortedItems.length).toBe(3);
      expect(sortedItems[0].title).toEqual('B');
      expect(sortedItems[1].title).toEqual('C');
      expect(sortedItems[2].title).toEqual('A');
    });
  });
});
