/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import AssessmentTemplate from '../assessment-template';
import {makeFakeInstance} from '../../../../js_specs/spec_helpers';

describe('AssessmentTemplate model', () => {
  let instance;

  beforeEach(() => {
    instance = makeFakeInstance({model: AssessmentTemplate})();
  });

  describe('form_preload method', () => {
    it('adds custom_attribute_definitions field', () => {
      expect(instance.custom_attribute_definitions)
        .toBeUndefined();

      instance.form_preload();

      expect(instance.custom_attribute_definitions instanceof can.List)
        .toBeTruthy();
    });
  });
});
