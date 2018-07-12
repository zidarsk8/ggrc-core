/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mappings from '../../../models/mappers/mappings';

describe('GGRC.Components.assessmentObjectTypeDropdown', function () {
  'use strict';

  let viewModel;

  beforeEach(function () {
    viewModel = GGRC.Components
      .getViewModel('assessmentObjectTypeDropdown');
  });

  it('returns the types obtained from the Mappings', function () {
    let result;

    let objectTypes = {
      groupFoo: {
        name: 'Foo Objects',
        items: [{name: 'Foo1'}, {value: 'Foo2'}],
      },
      groupBar: {
        name: 'Bar Objects',
        items: [{value: 'Bar1'}, {value: 'Bar2'}],
      },
    };

    spyOn(Mappings, 'getMappingTypes').and.returnValue(objectTypes);
    result = viewModel.attr('objectTypes');
    expect(result).toEqual(objectTypes);
  });

  it('sorts types within a group by name', function () {
    let result;

    let objectTypes = {
      groupFoo: {
        name: 'Bar-ish Objects',
        items: [
          {name: 'Car'}, {name: 'Bar'}, {name: 'Zar'}, {name: 'Dar'},
        ],
      },
    };

    let expected = [
      {name: 'Bar'}, {name: 'Car'}, {name: 'Dar'}, {name: 'Zar'},
    ];

    spyOn(Mappings, 'getMappingTypes').and.returnValue(objectTypes);

    result = viewModel.attr('objectTypes');
    expect(result.groupFoo.items).toEqual(expected);
  });

  it('omits the all_objects group from result', function () {
    let result;

    let objectTypes = {
      all_objects: {
        models: ['Foo', 'Bar', 'Baz'],
        name: 'FooBarBaz-type Objects',
      },
    };

    spyOn(Mappings, 'getMappingTypes').and.returnValue(objectTypes);

    result = viewModel.attr('objectTypes');
    expect(result.all_objects).toBeUndefined();
  });

  it('omits the types not relevant to the AssessmentTemplate from result',
    function () {
      let result;

      let objectTypes = {
        groupFoo: {
          name: 'Foo Objects',
          items: [
            {value: 'Contract'},  // this object type is relevant
            {value: 'Assessment'},
            {value: 'Audit'},
            {value: 'CycleTaskGroupObjectTask'},
          ],
        },
        groupBar: {
          name: 'Bar Objects',
          items: [
            {value: 'Policy'},  // this object type is relevant
            {value: 'TaskGroup'},
            {value: 'TaskGroupTask'},
          ],
        },
        groupBaz: {
          name: 'Baz Objects',
          items: [
            {value: 'Workflow'},
          ],
        },
      };

      let expected = {
        groupFoo: {
          name: 'Foo Objects',
          items: [{value: 'Contract'}],
        },
        groupBar: {
          name: 'Bar Objects',
          items: [{value: 'Policy'}],
        },
        // the groupBaz group, being empty, is expected to have been removed
      };

      spyOn(Mappings, 'getMappingTypes').and.returnValue(objectTypes);

      result = viewModel.attr('objectTypes');
      expect(result).toEqual(expected);
    }
  );
});
