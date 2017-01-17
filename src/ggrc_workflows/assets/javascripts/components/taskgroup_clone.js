  /*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

  can.Component.extend({
    tag: "task-group-clone",
    template: "<content/>",
    events: {
      click: function(el) {
        var $target;

        $target = $('<div class="modal hide"></div>').uniqueId();
        $target.modal_form({}, el);
        $target.ggrc_controllers_modals({
          modal_title: "Clone Task Group",
          model: CMS.ModelHelpers.CloneTaskGroup,
          instance: new CMS.ModelHelpers.CloneTaskGroup({ source_task_group: this.scope.taskGroup }),
          content_view: GGRC.mustache_path + "/task_groups/clone_modal_content.mustache",
          custom_save_button_text: "Proceed",
          button_view: GGRC.Controllers.Modals.BUTTON_VIEW_SAVE_CANCEL
        });
      }
    }
  });
})(window.GGRC, window.can);
