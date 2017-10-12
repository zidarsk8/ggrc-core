/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.attachButton', function () {
  'use strict';

  var viewModel;

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('attachButton');
    viewModel.attr('instance', new CMS.Models.Assessment());
  });

  describe('itemsUploadedCallback() method', function () {
    it('dispatches "refreshInstance" event', function () {
      spyOn(viewModel.instance, 'dispatch');
      viewModel.itemsUploadedCallback();

      expect(viewModel.instance.dispatch)
        .toHaveBeenCalledWith('refreshInstance');
    });

    it('does not throw error if instance is not provided', function () {
      viewModel.removeAttr('instance');

      expect(viewModel.itemsUploadedCallback.bind(viewModel))
        .not.toThrowError();
    });
  });
});
