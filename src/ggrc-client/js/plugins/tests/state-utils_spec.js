/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import * as StateUtils from '../utils/state-utils';
import * as CurrentPageUtils from '../utils/current-page-utils';

describe('StateUtils', function () {
  describe('statusFilter() method', function () {
    it('statusFilter() should return filter with all statuses',
      function () {
        let statuses = [
          'Draft', 'Active', 'Deprecated'
        ];

        let statesFilter = StateUtils.statusFilter(statuses, '');

        expect(statesFilter.indexOf('"Status"="Active"') > -1)
          .toBe(true);
        expect(statesFilter.indexOf('"Status"="Draft"') > -1)
          .toBe(true);
        expect(statesFilter.indexOf('"Status"="Deprecated"') > -1)
          .toBe(true);
      }
    );

    it('statesFilter should not update Assessmnet statuses',
      function () {
        let statuses = [
          'Not Started', 'In Progress', 'In Review'
        ];

        let statesFilter = StateUtils.statusFilter(statuses, '', 'Assessment');

        expect(statesFilter.indexOf('"Status"="Not Started"') > -1)
          .toBe(true);
        expect(statesFilter.indexOf('"Status"="In Progress"') > -1)
          .toBe(true);
        expect(statesFilter.indexOf('"Status"="In Review"') > -1)
          .toBe(true);
        expect(statesFilter.indexOf('"Status"="verified="') > -1)
          .toBe(false);
      }
    );

    it('statesFilter should have "Completed" status and "verified=true"',
      function () {
        let statuses = [
          'In Review', 'Completed and Verified'
        ];

        let statesFilter = StateUtils.statusFilter(statuses, '', 'Assessment');

        expect(statesFilter.indexOf('"Status"="In Review"') > -1)
          .toBe(true);
        expect(statesFilter.indexOf('"Status"="Completed"') > -1)
          .toBe(true);
        expect(statesFilter.indexOf('"Status"="Completed and Verified"') > -1)
          .toBe(false);

        expect(statesFilter.indexOf('verified=true') > -1)
          .toBe(true);
      }
    );

    it('statesFilter should have "Completed" status and "verified=false"',
      function () {
        let statuses = [
          'In Review', 'Completed (no verification)'
        ];

        let statesFilter = StateUtils.statusFilter(statuses, '', 'Assessment');

        expect(statesFilter.indexOf('"Status"="In Review"') > -1)
          .toBe(true);
        expect(statesFilter.indexOf('"Status"="Completed"') > -1)
          .toBe(true);
        expect(statesFilter
          .indexOf('"Status"="Completed (no verification)"') > -1)
          .toBe(false);

        expect(statesFilter.indexOf('verified=false') > -1)
          .toBe(true);
      }
    );

    it('statesFilter should have "Completed" status',
      function () {
        let statuses = [
          'In Progress', 'Completed (no verification)',
          'Completed and Verified'
        ];

        let statesFilter = StateUtils.statusFilter(statuses, '', 'Assessment');

        expect(statesFilter.indexOf('"Status"="In Progress"') > -1)
          .toBe(true);
        expect(statesFilter.indexOf('"Status"="Completed"') > -1)
          .toBe(true);

        expect(statesFilter
          .indexOf('"Status"="Completed (no verification)"') > -1)
          .toBe(false);
        expect(statesFilter
          .indexOf('"Status"="Completed and Verified"') > -1)
          .toBe(false);

        expect(statesFilter.indexOf('verified=') > -1)
          .toBe(false);
      }
    );
  });

  describe('getDefaultStatesForModel() method', function () {
    it('get default states for "MyAssessments" page', function () {
      let defaultStates;

      spyOn(CurrentPageUtils, 'isMyAssessments')
        .and.returnValue(true);

      defaultStates = StateUtils.getDefaultStatesForModel('Assessment');

      expect(defaultStates.length).toEqual(2);
      expect(defaultStates[0]).toEqual('Not Started');
    });

    it('get default states for "Control" type', function () {
      let defaultStates;

      spyOn(CurrentPageUtils, 'isMyAssessments')
        .and.returnValue(false);

      defaultStates = StateUtils.getDefaultStatesForModel('Control');

      expect(defaultStates.length).toEqual(3);
      expect(defaultStates[0]).toEqual('Active');
    });
  });

  describe('getStatusFieldName() method', function () {
    it('returns "Task State" for CycleTaskGroupObjectTask', function () {
      let expected = 'Task State';

      let actual = StateUtils.getStatusFieldName('CycleTaskGroupObjectTask');

      expect(actual).toEqual(expected);
    });

    it('returns "Status" when model is not provided', function () {
      let expected = 'Status';

      let actual = StateUtils.getStatusFieldName('');

      expect(actual).toEqual(expected);
    });

    it('returns "Status" for non-CycleTaskGroupObjectTask models',
      function () {
        let models = ['Standard', 'Regulation', 'Section', 'Objective',
          'Control', 'Product', 'System', 'Process', 'AccessGroup',
          'Assessment', 'Clause', 'Contract', 'DataAsset', 'Facility',
          'Issue', 'Market', 'OrgGroup', 'Policy', 'Program', 'Project',
          'Risk', 'Threat', 'Vendor', 'Audit', 'RiskAssessment', 'Workflow',
          'AssessmentTemplate', 'Person', 'TaskGroup', 'TaskGroupTask',
          'Cycle', 'CycleTaskGroup'];

        _.forEach(models, function (model) {
          expect(StateUtils.getStatusFieldName(model))
            .toEqual('Status');
        });
      });
  });

  describe('getBulkStatesForModel() method', function () {
    it('returns expected states for CycleTaskGroupObjectTask', function () {
      let expected = ['InProgress', 'Finished',
        'Declined', 'Deprecated', 'Verified'];

      let actual = StateUtils
        .getBulkStatesForModel('CycleTaskGroupObjectTask');

      expect(actual).toEqual(expected);
    });

    it('returns an empty array when model is not provided', function () {
      let expected = [];

      let actual = StateUtils.getBulkStatesForModel('');

      expect(actual).toEqual(expected);
    });

    it('returns an empty array for non-CycleTaskGroupObjectTask models',
      function () {
        let expected = [];
        let models = ['Standard', 'Regulation', 'Section', 'Objective',
          'Control', 'Product', 'System', 'Process', 'AccessGroup',
          'Assessment', 'Clause', 'Contract', 'DataAsset', 'Facility',
          'Issue', 'Market', 'OrgGroup', 'Policy', 'Program', 'Project',
          'Risk', 'Threat', 'Vendor', 'Audit', 'RiskAssessment', 'Workflow',
          'AssessmentTemplate', 'Person', 'TaskGroup', 'TaskGroupTask',
          'Cycle', 'CycleTaskGroup'];

        _.forEach(models, function (model) {
          expect(StateUtils.getBulkStatesForModel(model))
            .toEqual(expected);
        });
      });
  });
});
