/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import Mappings from '../../models/mappers/mappings';

(function (GGRC, can) {
  'use strict';

  GGRC.Components('assessmentObjectTypeDropdown', {
    tag: 'assessment-object-type-dropdown',
    viewModel: {
      define: {
        objectTypes: {
          get: function () {
            let self = this;
            let objectTypes = Mappings
              .getMappingTypes('AssessmentTemplate', [], ['Issue']);
            // remove ignored types and sort the rest
            _.each(objectTypes, function (objGroup) {
              objGroup.items = _.filter(objGroup.items, function (item) {
                return !self.getNonRelevantObjectTypes()[item.value];
              });
              objGroup.items = _.sortBy(objGroup.items, 'name');
            });

            // remove the groups that have ended up being empty
            objectTypes = _.pick(objectTypes, function (objGroup) {
              return objGroup.items && objGroup.items.length > 0;
            });

            return objectTypes;
          },
        },
      },
      assessmentType: '',
      instance: {},
      getNonRelevantObjectTypes: function () {
        return Object.freeze({
          AssessmentTemplate: true,
          Assessment: true,
          Audit: true,
          CycleTaskGroupObjectTask: true,
          TaskGroup: true,
          TaskGroupTask: true,
          Workflow: true,
        });
      },
    },
  });
})(window.GGRC, window.can);
