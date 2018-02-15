/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import Component from '../related-assessments';
import {getComponentVM} from '../../../../js_specs/spec_helpers';
import * as caUtils from '../../../plugins/utils/ca-utils';

describe('GGRC.Components.relatedAssessments', () => {
  describe('viewModel scope', () => {
    let originalModels;
    let viewModel;

    beforeEach(() => {
      viewModel = getComponentVM(Component);
    });

    describe('relativeObjectsTitle get() method', () => {
      beforeAll(() => {
        originalModels = CMS.Models;
      });

      afterAll(() => {
        CMS.Models = originalModels;
      });

      it('returns title based on instance.assessment_type', () => {
        let asmtModelType = 'Model1';
        let modelPlural = 'Awesome_models1';
        let expectedTitle;

        CMS.Models = {
          [asmtModelType]: {
            model_plural: modelPlural,
          },
        };
        viewModel.attr('instance.assessment_type', asmtModelType);
        expectedTitle = `Related ${modelPlural}`;

        expect(viewModel.attr('relatedObjectsTitle')).toBe(expectedTitle);
      });

      it(`returns title based on instance.type if is gotten related
          assessments not from assessment info pane`, () => {
        let modelType = 'Model1';
        let modelPlural = 'Awesome_models1';
        let expectedTitle;

        CMS.Models = {
          [modelType]: {
            model_plural: modelPlural,
          },
        };
        viewModel.attr('instance.assessment_type', null);
        viewModel.attr('instance.type', modelType);
        expectedTitle = `Related ${modelPlural}`;

        expect(viewModel.attr('relatedObjectsTitle')).toBe(expectedTitle);
      });
    });

    describe('loadRelatedAssessments() method', () => {
      const mockRelatedAsmtResponse = (response) => {
        spyOn(viewModel.attr('instance'), 'getRelatedAssessments')
          .and.returnValue(can.Deferred().resolve(response));
      };

      beforeEach(() => {
        spyOn(caUtils, 'prepareCustomAttributes');

        viewModel.attr('instance', {
          getRelatedAssessments() {},
        });
      });

      it('should not initialize the base array if response is empty',
        (done) => {
          mockRelatedAsmtResponse({
            total: 0,
            data: [],
          });

          viewModel.loadRelatedAssessments().then(() => {
            expect(viewModel.attr('paging.total')).toEqual(0);
            expect(viewModel.attr('relatedAssessments').length).toEqual(0);
            done();
          });
        });

      it('should initialize a base array', (done) => {
        mockRelatedAsmtResponse({
          total: 42,
          data: [{}, {}, {}, {}],
        });

        viewModel.loadRelatedAssessments().then(() => {
          let relAsmt = viewModel.attr('relatedAssessments');

          expect(viewModel.attr('paging.total')).toEqual(42);
          expect(relAsmt.length).toEqual(4);
          expect(relAsmt.filter((el) => el.instance).length).toEqual(4);
          done();
        });
      });

      it('should reset the loading flag after an error', (done) => {
        const relatedAssessments = viewModel.attr('relatedAssessments');

        spyOn(viewModel.attr('instance'), 'getRelatedAssessments')
          .and.returnValue(can.Deferred().reject());

        spyOn(relatedAssessments, 'replace');

        viewModel.loadRelatedAssessments().always(() => {
          expect(relatedAssessments.replace).not.toHaveBeenCalled();
          expect(caUtils.prepareCustomAttributes).not.toHaveBeenCalled();
          expect(viewModel.attr('loading')).toEqual(false);
          done();
        });
      });
    });
  });
});
