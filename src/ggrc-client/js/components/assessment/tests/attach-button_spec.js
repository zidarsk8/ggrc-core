/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import * as gDriveUtils from '../../../plugins/utils/gdrive-picker-utils';
import {makeFakeInstance} from '../../../../js_specs/spec_helpers';
import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../attach-button';
import Assessment from '../../../models/business-models/assessment';

describe('attach-button component', function () {
  'use strict';

  let viewModel;

  beforeEach(function () {
    viewModel = getComponentVM(Component);
    viewModel.attr('instance',
      makeFakeInstance({model: Assessment})()
    );
  });

  describe('finish() method', function () {
    it('dispatches "finish" event', function () {
      spyOn(viewModel, 'dispatch');
      viewModel.finish();

      expect(viewModel.dispatch)
        .toHaveBeenCalledWith('finish');
    });
  });

  describe('checkFolder() method', function () {
    it('should set isFolderAttached to true when folder is attached',
      function () {
        viewModel.attr('isFolderAttached', false);
        viewModel.attr('instance.folder', 'gdrive_folder_id');

        spyOn(viewModel, 'findFolder').and
          .returnValue($.Deferred().resolve({}));

        viewModel.checkFolder();
        expect(viewModel.attr('isFolderAttached')).toBe(true);
      });

    it('should set isFolderAttached to false when folder is not attached',
      function () {
        viewModel.attr('isFolderAttached', true);
        viewModel.attr('instance.folder', null);

        spyOn(viewModel, 'findFolder').and
          .returnValue($.Deferred().resolve());

        viewModel.checkFolder();
        expect(viewModel.attr('isFolderAttached')).toBe(false);
      });

    it('set correct isFolderAttached if instance refreshes during ' +
      'request to GDrive', function () {
      let dfd = $.Deferred();
      spyOn(gDriveUtils, 'findGDriveItemById').and.returnValue(dfd);

      viewModel.attr('instance.folder', 'gdrive_folder_id');
      viewModel.checkFolder(); // makes request to GDrive

      // instance is refreshed and folder becomes null
      viewModel.attr('instance.folder', null);
      viewModel.checkFolder();

      // resolve request to GDrive after instance refreshing
      dfd.resolve({folderId: 'gdrive_folder_id'});

      expect(viewModel.attr('isFolderAttached')).toBe(false);
    });
  });
});
