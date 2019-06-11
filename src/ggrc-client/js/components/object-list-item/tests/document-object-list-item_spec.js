/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../document-object-list-item';

describe('document-object-list-item component', () => {
  let viewModel;

  beforeEach(() => {
    viewModel = getComponentVM(Component);
  });

  describe('expect getter for', () => {
    it('itemData returns "instance"', () => {
      const instance = new can.Map({
        kind: 'listItem',
      });
      viewModel.attr('instance', instance);

      expect(viewModel.attr('itemData')).toEqual(instance);
    });

    it('itemTitle returns "instance.title" if defined', () => {
      const instance = new can.Map({
        title: 'Some Title',
        link: 'Some Link',
      });
      viewModel.attr('instance', instance);

      expect(viewModel.attr('itemTitle')).toEqual(instance.title);
    });

    it('itemTitle returns "instance.link" if title not defined', () => {
      const instance = new can.Map({
        title: null,
        link: 'Some Link',
      });
      viewModel.attr('instance', instance);

      expect(viewModel.attr('itemTitle')).toEqual(instance.link);
    });

    it('itemCreationDate returns "instance.created_at"', () => {
      const instance = new can.Map({
        created_at: Date.now(),
      });
      viewModel.attr('instance', instance);

      expect(viewModel.attr('itemCreationDate')).toEqual(instance.created_at);
    });

    it('itemStatus returns "instance.status"', () => {
      const instance = new can.Map({
        status: 'SomeState',
      });
      viewModel.attr('instance', instance);

      expect(viewModel.attr('itemStatus')).toEqual(instance.status);
    });

    it('isItemValid returns false if "instance.status" is "Deprecated"', () => {
      const instance = new can.Map({
        status: 'DepRecAted',
      });
      viewModel.attr('instance', instance);

      expect(viewModel.attr('isItemValid')).toBeFalsy();
    });

    it('isItemValid returns true if "instance.status" is not "Deprecated"',
      () => {
        const instance = new can.Map({
          status: 'Active',
        });
        viewModel.attr('instance', instance);

        expect(viewModel.attr('isItemValid')).toBeTruthy();
      });
  });
});
