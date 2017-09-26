  /*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import workflowHelpers from './workflow-helpers';

export default can.Component.extend({
  tag: 'workflow-start-cycle',
  content: '<content/>',
  events: {
    click: function () {
      var workflow = GGRC.page_instance();
      workflowHelpers.generateCycle(workflow);
    },
  },
});
