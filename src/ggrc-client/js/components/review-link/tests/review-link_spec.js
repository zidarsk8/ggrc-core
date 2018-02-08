/*
 Copyright (C) 2018 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../review-link';

describe('review-link component', () => {
  let viewModel;

  beforeAll(() => {
    viewModel = getComponentVM(Component);
  });

  describe('"checkMapping" function', () => {
    let method;

    beforeAll(() => {
      method = viewModel.checkMapping.bind(viewModel);
    });

    it('"isLoaded" should be false. instance is null', () => {
      viewModel.attr('instance', null);
      method();

      expect(viewModel.attr('isLoaded')).toBeFalsy();
    });

    it('"isLoaded" should be false. ' +
    'instance does not have "get_list_counter" function', () => {
      viewModel.attr('instance', {});
      method();

      expect(viewModel.attr('isLoaded')).toBeFalsy();
    });

    it('"isLoaded" should be true. "mappingExists" is false', (done) => {
      const dfd = can.Deferred();
      const instance = {
        get_list_counter: () => {
          return dfd.resolve();
        },
      };

      viewModel.attr('instance', instance);

      method();
      dfd.then(() => {
        expect(viewModel.attr('isLoaded')).toBeTruthy();
        expect(viewModel.attr('mappingExists')).toBeFalsy();
        done();
      });
    });

    it('"mappingExists" should be true', (done) => {
      const dfd = can.Deferred();
      const instance = {
        get_list_counter: () => {
          return dfd.resolve(1);
        },
      };

      viewModel.attr('instance', instance);

      method();
      dfd.then(() => {
        expect(viewModel.attr('isLoaded')).toBeTruthy();
        expect(viewModel.attr('mappingExists')).toBeTruthy();
        done();
      });
    });

    it('"mappingExists" should be true. "get_list_counter" returns function',
      (done) => {
        const dfd = can.Deferred();
        const instance = {
          get_list_counter: () => {
            return dfd.resolve(() => 1);
          },
        };

        viewModel.attr('instance', instance);

        method();
        dfd.then(() => {
          expect(viewModel.attr('isLoaded')).toBeTruthy();
          expect(viewModel.attr('mappingExists')).toBeTruthy();
          done();
        });
      }
    );
  });
});
