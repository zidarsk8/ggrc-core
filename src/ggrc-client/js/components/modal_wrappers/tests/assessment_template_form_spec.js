/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getComponentVM} from '../../../../js_specs/spec_helpers';
import Component from '../assessment_template_form';

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
});
