/*!
  Copyright (C) 2016 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: peter@reciprocitylabs.com
  Maintained By: peter@reciprocitylabs.com
*/

describe('can.Model.AssessmentTemplate', function () {
  'use strict';

  var AssessmentTemplate;
  var instance;  // an AssessmentTemplate instance

  beforeAll(function () {
    AssessmentTemplate = CMS.Models.AssessmentTemplate;
  });

  beforeEach(function () {
    instance = new AssessmentTemplate();
  });

  describe('_choosableObjectTypes() method', function () {
    var fakeMapper;  // an instance of the fake MapperModel
    var origMapperModel;

    beforeEach(function () {
      var FakeMapperModel;

      origMapperModel = GGRC.Models.MapperModel;

      // mock the MapperModel used by the method under test
      fakeMapper = {
        types: jasmine.createSpy()
      };
      FakeMapperModel = jasmine.createSpy().and.callFake(function (config) {
        return fakeMapper;
      });

      GGRC.Models.MapperModel = FakeMapperModel;
    });

    afterEach(function () {
      // restore the mocked MapperModel
      GGRC.Models.MapperModel = origMapperModel;
    });

    it('returns the types obtained from the mapper model', function () {
      var result;

      var objectTypes = {
        groupFoo: {
          name: 'Foo Objects',
          items: [{name: 'Foo1'}, {value: 'Foo2'}]
        },
        groupBar: {
          name: 'Bar Objects',
          items: [{value: 'Bar1'}, {value: 'Bar2'}]
        }
      };

      fakeMapper.types.and.returnValue(objectTypes);
      result = instance._choosableObjectTypes();
      expect(result).toEqual(objectTypes);
    });

    it('sorts types within a group by name', function () {
      var result;

      var objectTypes = {
        groupFoo: {
          name: 'Bar-ish Objects',
          items: [
            {name: 'Car'}, {name: 'Bar'}, {name: 'Zar'}, {name: 'Dar'}
          ]
        }
      };

      var expected = [
        {name: 'Bar'}, {name: 'Car'}, {name: 'Dar'}, {name: 'Zar'}
      ];

      fakeMapper.types.and.returnValue(objectTypes);
      result = instance._choosableObjectTypes();
      expect(result.groupFoo.items).toEqual(expected);
    });

    it('omits the all_objects group from result', function () {
      var result;

      var objectTypes = {
        all_objects: {
          models: ['Foo', 'Bar', 'Baz'],
          name: 'FooBarBaz-type Objects'
        }
      };

      fakeMapper.types.and.returnValue(objectTypes);
      result = instance._choosableObjectTypes();
      expect(result.all_objects).toBeUndefined();
    });

    it('omits the types not relevant to the AssessmentTemplate from result',
      function () {
        var result;

        var objectTypes = {
          groupFoo: {
            name: 'Foo Objects',
            items: [
              {value: 'Contract'},  // this object type is relevant
              {value: 'Assessment'},
              {value: 'Audit'},
              {value: 'CycleTaskGroupObjectTask'},
              {value: 'Request'}
            ]
          },
          groupBar: {
            name: 'Bar Objects',
            items: [
              {value: 'Policy'},  // this object type is relevant
              {value: 'TaskGroup'},
              {value: 'TaskGroupTask'}
            ]
          },
          groupBaz: {
            name: 'Baz Objects',
            items: [
              {value: 'Workflow'}
            ]
          }
        };

        var expected = {
          groupFoo: {
            name: 'Foo Objects',
            items: [{value: 'Contract'}]
          },
          groupBar: {
            name: 'Bar Objects',
            items: [{value: 'Policy'}]
          }
          // the groupBaz group, being empty, is expected to have been removed
        };

        fakeMapper.types.and.returnValue(objectTypes);
        result = instance._choosableObjectTypes();
        expect(result).toEqual(expected);
      }
    );
  });

  describe('_packPeopleData() method', function () {
    it('packs default people data into a JSON string', function () {
      var result;
      instance.attr('default_assessors', 'Rabbits');
      instance.attr('default_verifiers', 'Turtles');

      result = instance._packPeopleData();

      expect(typeof result).toEqual('string');
      result = JSON.parse(result);
      expect(result).toEqual({
        assessors: 'Rabbits',
        verifiers: 'Turtles'
      });
    });

    it('uses the user-provided list if assessors set to "other"', function () {
      var result;
      instance.attr('default_assessors', 'other');
      instance.attr('assessors_list', '  John,, Jack Mac,John,  Jill,  , ');
      instance.attr('default_verifiers', 'Whatever');

      result = instance._packPeopleData();

      expect(typeof result).toEqual('string');
      result = JSON.parse(result);
      expect(result).toEqual({
        assessors: ['John', 'Jack Mac', 'Jill'],
        verifiers: 'Whatever'
      });
    });

    it('uses the user-provided list if verifiers set to "other"', function () {
      var result;
      instance.attr('default_assessors', 'Whatever');
      instance.attr('default_verifiers', 'other');
      instance.attr('verifiers_list', '  First, ,, Sec ond   ,First, Third ');

      result = instance._packPeopleData();

      expect(typeof result).toEqual('string');
      result = JSON.parse(result);
      expect(result).toEqual({
        assessors: 'Whatever',
        verifiers: ['First', 'Sec ond', 'Third']
      });
    });
  });
});
