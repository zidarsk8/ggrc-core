/*
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import ModalsController from '../../../../ggrc/assets/javascripts/controllers/modals_controller';
import {BUTTON_VIEW_SAVE_CANCEL} from '../../../../ggrc/assets/javascripts/plugins/utils/modals';

export default ModalsController({
  pluginName: 'ggrc_controllers_approval_workflow',
  defaults : {
    original_object : null,
    new_object_form: true,
    model: CMS.ModelHelpers.ApprovalWorkflow,
    modal_title: "Submit for review",
    custom_save_button_text: "Submit",
    content_view: GGRC.mustache_path + "/wf_objects/approval_modal_content.mustache",
    button_view : BUTTON_VIEW_SAVE_CANCEL,
    afterFetch: function () {
      this.attr("instance", new CMS.ModelHelpers.ApprovalWorkflow({
        original_object : this.attr('instance')
      }));
    }
  }
}, {
  init : function() {
    this.options.button_view = BUTTON_VIEW_SAVE_CANCEL;
    this._super.apply(this, arguments);
  },
  "input[null-if-empty] change" : function(el, ev) {
    if(el.val() === "") {
      this.options.instance.attr(el.attr("name").split(".").slice(0, -1).join("."), null);
    }
  }
});
