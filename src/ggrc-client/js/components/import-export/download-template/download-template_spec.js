/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from './download-template';
import * as Utils from '../../../plugins/utils/import-export-utils';
import {backendGdriveClient} from '../../../plugins/ggrc-gapi-client';
import * as ModalsUtils from '../../../plugins/utils/modals';

describe('download-template component', () => {
  let vm;

  beforeEach(() => {
    vm = getComponentVM(Component);
  });

  describe('selectItems method', () => {
    it('should fill selected array from event', () => {
      vm.selectItems({
        selected: [{name: 'Foo'}, {name: 'Bar'}, {name: 'Baz'}],
      });

      let selected = Array.from(vm.attr('selected').map(({name}) => name));

      expect(selected.length).toEqual(3);
      expect(selected).toEqual(['Foo', 'Bar', 'Baz']);
    });

    it('should reset selected array after uncheck all items', () => {
      vm.attr('selected', ['Foo', 'Bar', 'Baz']);

      vm.selectItems({
        selected: [],
      });

      expect(vm.attr('selected').length).toEqual(0);
    });

    it('should reset selected array if event does not contain data', () => {
      vm.attr('selected', ['Foo', 'Bar', 'Baz']);

      vm.selectItems({});

      expect(vm.attr('selected').length).toEqual(0);
    });
  });

  describe('downloadCSV method', () => {
    it('should do ajax call in proper format', (done) => {
      spyOn(Utils, 'downloadTemplate')
        .and.returnValue($.Deferred().resolve('FooBar'));
      spyOn(Utils, 'download');

      vm.attr('selected', [{name: 'Foo'}, {name: 'Bar'}, {name: 'Baz'}]);

      vm.downloadCSV().then(() => {
        expect(Utils.downloadTemplate)
          .toHaveBeenCalledWith({
            data: {
              objects: [
                {object_name: 'Foo'},
                {object_name: 'Bar'},
                {object_name: 'Baz'},
              ],
              export_to: 'csv',
            },
          });
        expect(Utils.download)
          .toHaveBeenCalledWith('import_template.csv', 'FooBar');
        expect(vm.attr('modalState.open')).toEqual(false);

        done();
      });
    });

    it('should not download CSV and should close the modal after error during' +
      '"downloadTemplate" phase', (done) => {
      spyOn(Utils, 'downloadTemplate')
        .and.returnValue($.Deferred().reject());
      spyOn(Utils, 'download');

      vm.attr('selected', [1, 2, 3]);

      vm.downloadCSV().fail(() => {
        expect(Utils.downloadTemplate).toHaveBeenCalled();
        expect(Utils.download).not.toHaveBeenCalled();
        expect(vm.attr('modalState.open')).toEqual(false);

        done();
      });
    });
  });

  describe('downloadSheet method', () => {
    let downloadSpy;

    beforeEach(() => {
      spyOn(backendGdriveClient, 'withAuth').and.callFake((callback) => {
        return callback();
      });
      spyOn(ModalsUtils, 'confirm');
      downloadSpy = spyOn(Utils, 'downloadTemplate');
    });

    it('should do ajax call in proper format', (done) => {
      downloadSpy.and.returnValue($.Deferred().resolve('FooBar'));

      vm.attr('selected', [{name: 'Foo'}, {name: 'Bar'}, {name: 'Baz'}]);

      vm.downloadSheet().then(() => {
        expect(backendGdriveClient.withAuth).toHaveBeenCalled();
        expect(Utils.downloadTemplate)
          .toHaveBeenCalledWith({
            data: {
              objects: [
                {object_name: 'Foo'},
                {object_name: 'Bar'},
                {object_name: 'Baz'},
              ],
              export_to: 'gdrive',
            },
          });
        expect(ModalsUtils.confirm).toHaveBeenCalled();
        expect(vm.attr('modalState.open')).toEqual(false);

        done();
      });
    });

    it('should not download Sheet and should close the modal after error' +
      'during "downloadTemplate" phase', (done) => {
      downloadSpy.and.returnValue($.Deferred().reject());

      vm.attr('selected', [1, 2, 3]);

      vm.downloadSheet().fail(() => {
        expect(backendGdriveClient.withAuth).toHaveBeenCalled();
        expect(Utils.downloadTemplate).toHaveBeenCalled();
        expect(ModalsUtils.confirm).not.toHaveBeenCalled();
        expect(vm.attr('modalState.open')).toEqual(false);

        done();
      });
    });
  });
});
