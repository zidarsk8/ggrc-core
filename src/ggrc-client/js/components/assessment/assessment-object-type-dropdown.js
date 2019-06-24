/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanComponent from 'can-component';
import {groupTypes} from '../../plugins/utils/models-utils';

export default CanComponent.extend({
  tag: 'assessment-object-type-dropdown',
  leakScope: true,
  viewModel: can.Map.extend({
    define: {
      objectTypes: {
        get: function () {
          let objectTypes = groupTypes(GGRC.config.snapshotable_objects);

          // remove the groups that have ended up being empty
          objectTypes = _.pickBy(objectTypes, function (objGroup) {
            return objGroup.items && objGroup.items.length > 0;
          });

          return objectTypes;
        },
      },
    },
    assessmentType: '',
    instance: {},
  }),
});
