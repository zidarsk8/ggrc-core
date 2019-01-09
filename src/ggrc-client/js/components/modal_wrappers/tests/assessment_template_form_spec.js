/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {
  getComponentVM,
  makeFakeInstance,
} from '../../../../js_specs/spec_helpers';
import Component from '../assessment_template_form';
import AssessmentTemplate from '../../../models/business-models/assessment-template';

const PEOPLE_VALUES_OPTIONS = Object.freeze({
  Control: [
    {value: 'Admin', title: 'Object Admins'},
    {value: 'Audit Lead', title: 'Audit Captain'},
    {value: 'Auditors', title: 'Auditors'},
    {value: 'Principal Assignees', title: 'Principal Assignees'},
    {value: 'Secondary Assignees', title: 'Secondary Assignees'},
    {value: 'Control Operators', title: 'Control Operators'},
    {value: 'Control Owners', title: 'Control Owners'},
    {value: 'Other Contacts', title: 'Other Contacts'},
    {value: 'other', title: 'Others...'},
  ],
  defaults: [
    {value: 'Admin', title: 'Object Admins'},
    {value: 'Audit Lead', title: 'Audit Captain'},
    {value: 'Auditors', title: 'Auditors'},
    {value: 'Principal Assignees', title: 'Principal Assignees'},
    {value: 'Secondary Assignees', title: 'Secondary Assignees'},
    {value: 'Primary Contacts', title: 'Primary Contacts'},
    {value: 'Secondary Contacts', title: 'Secondary Contacts'},
    {value: 'other', title: 'Others...'},
  ],
});

describe('wrapper-assessment-template component', function () {
  let viewModel;

  beforeEach(function () {
    viewModel = getComponentVM(Component);
  });

  describe('getter for showCaptainAlert', function () {
    it('sets showCaptainAlert is true if default_people.assignees ' +
    'in peopleTitlesList array', function () {
      viewModel.attr('instance.default_people', {assignees: 'Auditors'});

      expect(viewModel.attr('showCaptainAlert')).toBe(true);
    });

    it('sets showCaptainAlert is false if default_people.assignees ' +
    'not in peopleTitlesList array', function () {
      viewModel.attr('instance.default_people', {assignees: 'People'});

      expect(viewModel.attr('showCaptainAlert')).toBe(false);
    });
  });

  describe('peopleValues property', () => {
    beforeEach(() => {
      let model = makeFakeInstance({model: AssessmentTemplate})();
      viewModel.attr('instance', model);
    });

    it('returns correct values when template_object_type is Control', () => {
      viewModel.attr('instance.template_object_type', 'Control');

      let peopleValues = viewModel.attr('peopleValues');
      expect(peopleValues)
        .toEqual(PEOPLE_VALUES_OPTIONS.Control);
    });

    it('returns default values when template_object_type is not Control',
      () => {
        viewModel.attr('instance.template_object_type', 'Metric');

        let peopleValues = viewModel.attr('peopleValues');
        expect(peopleValues)
          .toEqual(PEOPLE_VALUES_OPTIONS.defaults);
      });
  });
});
