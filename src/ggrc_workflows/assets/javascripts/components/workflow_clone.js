  /*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

  can.Component.extend({
    tag: "workflow-clone",
    template: "<content/>",
    events: {
      click: function(el) {
        var workflow, $target;

        $target = $('<div class="modal hide"></div>').uniqueId();
        $target.modal_form({}, el);
        $target.ggrc_controllers_modals({
          modal_title: "Clone Workflow",
          model: CMS.ModelHelpers.CloneWorkflow,
          instance: new CMS.ModelHelpers.CloneWorkflow({ source_workflow: this.scope.workflow }),
          content_view: GGRC.mustache_path + "/workflows/clone_modal_content.mustache",
          custom_save_button_text: "Proceed",
          button_view: GGRC.Controllers.Modals.BUTTON_VIEW_SAVE_CANCEL
        });
      }
    }
  });
})(window.GGRC, window.can);
