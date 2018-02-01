/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import * as pickerUtils from '../../../plugins/utils/gdrive-picker-utils';

describe('GGRC.Components.gDrivePickerLauncher', function () {
  'use strict';

  let viewModel;
  const optsAuditFolder = {
    dest: {
      id: 'some-folder-id',
    },
  };
  const optsWithoutAuditFolder = {};
  const ROOT_FOLDER_ID = 'root-folder-id';
  const FILE_NEW_UPLOAD = 'FILE_NEW_UPLOAD';
  const FILE_PICKED = 'FILE_PICKED';

  function genUploadedFile(
    fileType = FILE_PICKED, parentFolderId = ROOT_FOLDER_ID, role = 'owner') {
    return {
      newUpload: fileType === FILE_NEW_UPLOAD,
      title: 'my-file.png',
      parents: [
        {
          isRoot: parentFolderId === ROOT_FOLDER_ID,
          id: parentFolderId,
        },
      ],
      userPermission: {
        id: 'me',
        role,
      },
    };
  }

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('gDrivePickerLauncher');
    viewModel.attr('instance', {
      slug: 'ASSESSMENT-1',
    });
    viewModel.attr('assessmentTypeObjects', [
      {revision: {content: {slug: 'CONTROL-345'}}},
      {revision: {content: {slug: 'CONTROL-678'}}},
    ]);

    spyOn(viewModel, 'runRenameBatch')
      .and.returnValue(new $.Deferred().resolve([]));
    spyOn(viewModel, 'refreshFilesModel')
      .and.returnValue(new $.Deferred().resolve([]));

    // expect(viewModel.runRenameBatch).toHaveBeenCalled();
    // expect(viewModel.refreshFilesModel).toHaveBeenCalled();
  });

  it('should test sanitizeSlug() method', function () {
    let sanitizationCheck = {
      'abc-test-code-1.CA-865': 'abc-test-code-1-ca-865',
      'AC01.CA-1121': 'ac01-ca-1121',

      'Automated E-Waste Dashboard.CA-935':
        'automated-e-waste-dashboard-ca-935',

      'CA.PCI 1.2.1': 'ca-pci-1-2-1',
      'control-13.CA-855': 'control-13-ca-855',
      'CONTROL-2084.CA-844': 'control-2084-ca-844',
      'PCI 10.4.3.CA-1065': 'pci-10-4-3-ca-1065',
      'REQUEST-957': 'request-957',
      'TV03.2.4.CA': 'tv03-2-4-ca',
      'SM05.CA-1178': 'sm05-ca-1178',
      'ASSESSMENT-12345': 'assessment-12345',
    };

    Object.keys(sanitizationCheck).forEach(function (key) {
      expect(viewModel.sanitizeSlug(key)).toBe(sanitizationCheck[key]);
    });
  });

  it('should test addFileSuffix() method', function () {
    let fakeInstance = new can.Map({
      slug: 'ASSESSMENT-12345',
    });

    let fileNameTransformationMap = {
      'Screenshot 2016-04-29 12.56.30.png':
        'Screenshot 2016-04-29 12.56.30_ggrc_assessment' +
        '-12345_control-345_control-678.png',

      'IMG-9000_ggrc_request-12345.jpg':
        'IMG-9000_ggrc_assessment-12345_control-345_control-678.jpg',
    };

    viewModel.attr('instance', fakeInstance);

    Object.keys(fileNameTransformationMap).forEach(function (key) {
      expect(viewModel.addFileSuffix(key)).toBe(fileNameTransformationMap[key]);
    });
  });

  /**
   * With Audit Folder
   */

  it('should edit newly uploaded file with Audit folder', function () {
    spyOn(viewModel, 'createEditRequest');
    spyOn(viewModel, 'createCopyRequest');

    viewModel.addFilesSuffixes(optsAuditFolder, [
      genUploadedFile(FILE_NEW_UPLOAD), // newly uploaded file to the root of My Drive
    ]);

    expect(viewModel.createEditRequest).toHaveBeenCalled();
    expect(viewModel.createCopyRequest).not.toHaveBeenCalled();
  });

  it('should copy file picked from random folder', function () {
    spyOn(viewModel, 'createEditRequest');
    spyOn(viewModel, 'createCopyRequest');

    viewModel.addFilesSuffixes(optsAuditFolder, [
      genUploadedFile(FILE_PICKED, 'some-random-folder'),
    ]);

    expect(viewModel.createEditRequest).not.toHaveBeenCalled();
    expect(viewModel.createCopyRequest).toHaveBeenCalled();
  });

  it('should reuse file picked from the same folder', function () {
    let file = genUploadedFile(FILE_PICKED, optsAuditFolder.dest.id);

    spyOn(viewModel, 'createEditRequest');
    spyOn(viewModel, 'createCopyRequest');

    // making the file name to already have a slug
    file.title = viewModel.addFileSuffix(file.title);
    viewModel.addFilesSuffixes(optsAuditFolder, [
      file,
    ]);

    expect(viewModel.createEditRequest).not.toHaveBeenCalled();
    expect(viewModel.createCopyRequest).not.toHaveBeenCalled();
  });

  it('should copy shared file', function () {
    spyOn(viewModel, 'createEditRequest');
    spyOn(viewModel, 'createCopyRequest');

    viewModel.addFilesSuffixes(optsAuditFolder, [
      genUploadedFile(FILE_PICKED, 'some-random-folder', 'reader'),
    ]);

    expect(viewModel.createEditRequest).not.toHaveBeenCalled();
    expect(viewModel.createCopyRequest).toHaveBeenCalled();
  });

  // -----------------

  /**
   * No Audit Folder
   */

  it('should edit newly uploaded file without Audit folder', function () {
    spyOn(viewModel, 'createEditRequest');
    spyOn(viewModel, 'createCopyRequest');

    viewModel.addFilesSuffixes(optsWithoutAuditFolder, [
      genUploadedFile(FILE_NEW_UPLOAD), // newly uploaded file to the root of My Drive
    ]);

    expect(viewModel.createEditRequest).toHaveBeenCalled();
    expect(viewModel.createCopyRequest).not.toHaveBeenCalled();
  });

  it('should copy file picked from random folder', function () {
    spyOn(viewModel, 'createEditRequest');
    spyOn(viewModel, 'createCopyRequest');

    viewModel.addFilesSuffixes(optsWithoutAuditFolder, [
      genUploadedFile(FILE_PICKED, 'some-random-folder'),
    ]);

    expect(viewModel.createEditRequest).not.toHaveBeenCalled();
    expect(viewModel.createCopyRequest).toHaveBeenCalled();
  });

  it('should reuse file picked from the same root folder', function () {
    let file = genUploadedFile(FILE_PICKED);

    spyOn(viewModel, 'createEditRequest');
    spyOn(viewModel, 'createCopyRequest');

    // making the file name to already have a slug
    file.title = viewModel.addFileSuffix(file.title);
    viewModel.addFilesSuffixes(optsWithoutAuditFolder, [
      file,
    ]);

    expect(viewModel.createEditRequest).not.toHaveBeenCalled();
    expect(viewModel.createCopyRequest).not.toHaveBeenCalled();
  });

  it('should copy shared file', function () {
    spyOn(viewModel, 'createEditRequest');
    spyOn(viewModel, 'createCopyRequest');

    viewModel.addFilesSuffixes(optsWithoutAuditFolder, [
      genUploadedFile(FILE_PICKED, 'some-random-folder', 'reader'),
    ]);

    expect(viewModel.createEditRequest).not.toHaveBeenCalled();
    expect(viewModel.createCopyRequest).toHaveBeenCalled();
  });
});

describe('GGRC.Components.gDrivePickerLauncher', function () {
  'use strict';

  let Component;
  let events;
  let viewModel;
  let eventStub = {
    preventDefault: function () {},
  };

  beforeAll(function () {
    Component = GGRC.Components.get('gDrivePickerLauncher');
    events = Component.prototype.events;
  });

  beforeEach(function () {
    viewModel = GGRC.Components.getViewModel('gDrivePickerLauncher');
  });

  describe('onClickHandler() method', function () {
    it('call confirmationCallback() if it is provided', function () {
      spyOn(viewModel, 'confirmationCallback');

      viewModel.onClickHandler(null, null, eventStub);

      expect(viewModel.confirmationCallback).toHaveBeenCalled();
    });

    it('pass callbackResult to can.when()', function () {
      let dfd = can.Deferred();
      let thenSpy = jasmine.createSpy('then');
      spyOn(viewModel, 'confirmationCallback').and.returnValue(dfd);
      spyOn(can, 'when').and.returnValue({
        then: thenSpy,
      });

      viewModel.onClickHandler(null, null, eventStub);

      expect(can.when).toHaveBeenCalledWith(dfd);
      expect(thenSpy).toHaveBeenCalled();
    });

    it('pass null to can.when() when callback is not provided', function () {
      let thenSpy = jasmine.createSpy('then');
      spyOn(can, 'when').and.returnValue({
        then: thenSpy,
      });

      viewModel.onClickHandler(null, null, eventStub);

      expect(can.when).toHaveBeenCalledWith(null);
      expect(thenSpy).toHaveBeenCalled();
    });
  });

  describe('onKeyup() method', function () {
    describe('if escape key was clicked', function () {
      let event;
      let element;

      beforeEach(function () {
        const ESCAPE_KEY_CODE = 27;
        event = {
          keyCode: ESCAPE_KEY_CODE,
          stopPropagation: jasmine.createSpy('stopPropagation'),
        };
        element = $('<div></div>');
      });

      it('calls stopPropagation for passed event', function () {
        viewModel.onKeyup(element, event);
        expect(event.stopPropagation).toHaveBeenCalled();
      });

      it('unsets focus for element', function (done) {
        const blur = function () {
          done();
          element.off('blur', blur);
        };
        element.on('blur', blur);
        viewModel.onKeyup(element, event);
      });
    });
  });

  describe('events', function () {
    describe('"{viewModel} modal:success" handler', function () {
      let method;
      let that;

      beforeEach(function () {
        that = {
          viewModel: viewModel,
        };
        method = events['{viewModel} modal:success'].bind(that);
      });

      it('calls callback if callback is provided', function () {
        viewModel.attr('itemsUploadedCallback', jasmine.createSpy('callback'));
        method();
        expect(viewModel.itemsUploadedCallback).toHaveBeenCalled();
      });

      it('refreshes instance if callback is not provided', function () {
        viewModel.instance = jasmine.createSpyObj('instance',
          ['reify', 'refresh']);
        method();
        expect(viewModel.instance.reify).toHaveBeenCalled();
        expect(viewModel.instance.refresh).toHaveBeenCalled();
      });
    });
  });

  describe('trigger_upload() method', function () {
    let uploadFilesDfd;
    let renameFileDfd;
    let el;

    beforeEach(function () {
      el = jasmine.createSpyObj(['data', 'trigger']);
      uploadFilesDfd = can.Deferred();
      spyOn(pickerUtils, 'uploadFiles').and.returnValue(uploadFilesDfd);
    });

    it('sets "isUploading" flag to true', function () {
      viewModel.attr('isUploading', false);

      viewModel.trigger_upload(viewModel, el);

      expect(viewModel.attr('isUploading')).toBe(true);
    });

    describe('sets "isUploading" flag to false', function () {
      beforeEach(function () {
        renameFileDfd = can.Deferred();
        viewModel.attr('isUploading', true);
        spyOn(viewModel, 'beforeCreateHandler');
        spyOn(viewModel, 'addFilesSuffixes').and.returnValue(renameFileDfd);
      });

      it('when uploadFiles() was failed', function () {
        uploadFilesDfd.reject();

        viewModel.trigger_upload(viewModel, el);

        expect(viewModel.attr('isUploading')).toBe(false);
      });

      it('after addFilesSuffixes() success', function () {
        uploadFilesDfd.resolve();
        renameFileDfd.resolve([]);

        viewModel.trigger_upload(viewModel, el);

        expect(viewModel.attr('isUploading')).toBe(false);
      });

      it('when addFilesSuffixes() was failed', function () {
        uploadFilesDfd.resolve();
        renameFileDfd.reject();

        viewModel.trigger_upload(viewModel, el);

        expect(viewModel.attr('isUploading')).toBe(false);
      });
    });
  });

  describe('trigger_upload_parent() method', function () {
    let uploadFilesDfd;
    let renameFileDfd;
    let parentFolderDfd;
    let el;
    let parentFolderStub;

    beforeEach(function () {
      el = jasmine.createSpyObj(['data', 'trigger']);
      parentFolderStub = {id: 'id'};
      parentFolderDfd = can.Deferred();
      uploadFilesDfd = can.Deferred();

      spyOn(pickerUtils, 'findGDriveItemById').and.returnValue(parentFolderDfd);
      spyOn(pickerUtils, 'uploadFiles').and.returnValue(uploadFilesDfd);
    });

    it('sets "isUploading" flag to true', function () {
      parentFolderDfd.resolve(parentFolderStub);
      viewModel.attr('isUploading', false);

      viewModel.trigger_upload_parent(viewModel, el);

      expect(viewModel.attr('isUploading')).toBe(true);
    });

    describe('sets "isUploading" flag to false', function () {
      beforeEach(function () {
        viewModel.attr('isUploading', true);
        spyOn(viewModel, 'addFilesSuffixes').and.returnValue(renameFileDfd);
        spyOn(viewModel, 'beforeCreateHandler')
          .and.returnValue(can.Deferred().resolve());
        renameFileDfd = can.Deferred();
      });

      it('after uploadFiles() success', function () {
        spyOn(viewModel, 'handle_file_upload')
          .and.returnValue(can.Deferred().resolve());
        parentFolderDfd.resolve(parentFolderStub);
        uploadFilesDfd.resolve();
        renameFileDfd.reject();

        viewModel.trigger_upload_parent(viewModel, el);

        expect(viewModel.attr('isUploading')).toBe(false);
      });

      it('when uploadFiles() was failed', function () {
        parentFolderDfd.resolve(parentFolderStub);
        uploadFilesDfd.reject();

        viewModel.trigger_upload_parent(viewModel, el);

        expect(viewModel.attr('isUploading')).toBe(false);
      });
    });
  });
});
