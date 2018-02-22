/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from './download-template';
import * as Utils from '../import-export-utils';

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
      spyOn(Utils, 'exportRequest')
        .and.returnValue(can.Deferred().resolve('FooBar'));
      spyOn(Utils, 'download');

      vm.attr('selected', [{name: 'Foo'}, {name: 'Bar'}, {name: 'Baz'}]);

      vm.downloadCSV().then(() => {
        expect(Utils.exportRequest)
          .toHaveBeenCalledWith({
            data: {
              objects: [
                {object_name: 'Foo', fields: 'all'},
                {object_name: 'Bar', fields: 'all'},
                {object_name: 'Baz', fields: 'all'},
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

    it('should not do ajax call if nothing selected', () => {
      spyOn(Utils, 'exportRequest');
      spyOn(Utils, 'download');

      vm.attr('selected', []);

      vm.downloadCSV();

      expect(Utils.exportRequest).not.toHaveBeenCalled();
      expect(Utils.download).not.toHaveBeenCalled();
    });

    it('should not download CSV and should close the modal after error during' +
      '"exportRequest" phase', (done) => {
      spyOn(Utils, 'exportRequest')
        .and.returnValue(can.Deferred().reject());
      spyOn(Utils, 'download');

      vm.attr('selected', [1, 2, 3]);

      vm.downloadCSV().fail(() => {
        expect(Utils.exportRequest).toHaveBeenCalled();
        expect(Utils.download).not.toHaveBeenCalled();
        expect(vm.attr('modalState.open')).toEqual(false);

        done();
      });
    });
  });
});
