  /*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import workflowHelpers from './workflow-helpers';

export default can.Component.extend({
  tag: 'workflow-start-cycle',
  content: '<content/>',
  events: {
    click: function () {
      let workflow = GGRC.page_instance();
      workflowHelpers.generateCycle(workflow)
        .then(function () {
          return workflow.refresh_all('task_groups', 'task_group_tasks');
        });
    },
  },
});
