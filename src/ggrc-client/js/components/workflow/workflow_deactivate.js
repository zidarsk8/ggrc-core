
  /*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

  can.Component.extend({
    tag: "workflow-deactivate",
    template: "<content/>",
    events: {
      click: function() {
        var workflow = GGRC.page_instance();
        workflow.refresh().then(function(workflow) {
          workflow.attr('recurrences', false).save();
        });
      }
    }
  });
})(window.GGRC, window.can);
