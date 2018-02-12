/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import * as SnapshotUtils from '../../../plugins/utils/snapshot-utils';
import ObjectOperationsBaseVM from '../object-operations-base-vm';

describe('ObjectOperationsBaseVM', function () {
  'use strict';

  let baseVM;

  beforeEach(function () {
    baseVM = ObjectOperationsBaseVM();
  });

  describe('availableTypes() method', function () {
    beforeAll(function () {
      spyOn(SnapshotUtils, 'getInScopeModels')
        .and.returnValue(['test1', 'test2']);
    });

    it('correctly calls getMappingTypes', function () {
      let result;
      spyOn(GGRC.Mappings, 'getMappingTypes').and.returnValue('types');
      baseVM.attr('object', 'testObject');

      result = baseVM.availableTypes();
      expect(GGRC.Mappings.getMappingTypes).toHaveBeenCalledWith('testObject',
        [], ['test1', 'test2', 'TaskGroup']);
      expect(result).toEqual('types');
    });
  });

  describe('get() for baseVM.parentInstance', function () {
    beforeEach(function () {
      spyOn(CMS.Models, 'get_instance')
        .and.returnValue('parentInstance');
    });

    it('returns parentInstance', function () {
      let result = baseVM.attr('parentInstance');
      expect(result).toEqual('parentInstance');
    });
  });

  describe('set() for baseVM.type', function () {
    let method;
    let vm;

    beforeEach(function () {
      vm = new can.Map({
        config: {
          general: {},
          special: [
            {
              types: ['Type1', 'Type2'],
              config: {},
            },
            {
              types: ['Type1'],
              config: {},
            },
          ],
        },
        update: jasmine.createSpy('update'),
        prepareConfig: jasmine.createSpy('prepareConfig'),
      });
      method = ObjectOperationsBaseVM
        .prototype
        .define
        .type
        .set.bind(vm);
    });

    it('sets passed type', function () {
      let type = 'Type1';
      let result = method(type);
      expect(result).toBe(type);
    });

    it('calls update method if type is set for the first time',
    function () {
      let type = 'Type1';
      method(type);
      expect(vm.update).toHaveBeenCalled();
    });

    it('removes "type" property from config passed in appopriate ' +
    'config handler', function () {
      let args;
      method('Type1');

      args = vm.update.calls.argsFor(0);
      expect(args[0]).not.toEqual(jasmine.objectContaining({
        type: jasmine.any(String),
      }));
    });

    it('calls prepareConfig method if type is defined',
    function () {
      vm.attr('type', 'Type1');
      method('Type1');
      expect(vm.prepareConfig).toHaveBeenCalled();
    });
  });

  describe('modelFromType() method', function () {
    it('returns undefined if no models', function () {
      let result = baseVM.modelFromType('program');
      expect(result).toEqual(undefined);
    });

    it('returns model config by model value', function () {
      let result;
      let types = {
        governance: {
          items: [{
            value: 'v1',
          }, {
            value: 'v2',
          }, {
            value: 'v3',
          }],
        },
      };

      spyOn(GGRC.Mappings, 'getMappingTypes')
        .and.returnValue(types);

      result = baseVM.modelFromType('v2');
      expect(result).toEqual(types.governance.items[1]);
    });
  });

  describe('update() method', function () {
    let baseConfig;
    let method;
    let vm;

    beforeEach(function () {
      baseConfig = {
        a: 'a',
        b: {
          c: 'c',
        },
      };
      vm = new can.Map(baseConfig);
      method = baseVM.update.bind(vm);
      spyOn(vm, 'attr').and.callThrough();
    });

    it('sets new values for VM', function () {
      let config = {
        a: 'new A',
        b: {
          h: 'new H',
        },
        c: [],
      };
      method(config);

      expect(vm.attr()).toEqual(config);
    });

    it('does not set values for VM from config if appopriate fields from ' +
    'VM and config have the same values', function () {
      let allArgs;
      method(baseConfig);

      allArgs = vm.attr.calls.allArgs();

      expect(_.every(allArgs, function (args) {
        return args.length === 1;
      })).toBe(true);
    });
  });

  describe('prepareConfig() method', function () {
    let method;
    let vm;

    beforeEach(function () {
      vm = {
        update: jasmine.createSpy('update'),
      };
      method = baseVM.prepareConfig.bind(vm);
    });

    it('calls update method with config from param', function () {
      let config = {};
      method(config);

      expect(vm.update).toHaveBeenCalledWith(config);
    });
  });

  describe('extractConfig() method', function () {
    let method;
    let config;

    beforeAll(function () {
      method = ObjectOperationsBaseVM.extractConfig;
    });

    beforeEach(function () {
      config = {
        general: {},
        special: [{
          types: ['T1', 'T2'],
          config: {},
        }, {
          types: ['T3'],
          config: {
            field: 1,
            field2: 2,
          },
        }],
      };
    });

    it('extracts general config if there is no special config for type',
    function () {
      let result = method('T0', config);
      expect(result).toBe(config.general);
    });

    it('extracts special config if there is special config for type',
    function () {
      let result = method('T2', config);
      expect(result).toEqual(config.special[0].config);
    });
  });
});
