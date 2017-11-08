/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import ModalsController from '../../../../ggrc/assets/javascripts/controllers/modals_controller';
import {BUTTON_VIEW_SAVE_CANCEL} from '../../../../ggrc/assets/javascripts/plugins/utils/modals';

;(function(can, $, GGRC, CMS) {

ModalsController({
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

GGRC.register_modal_hook("approvalform", function($target, $trigger, option) {
  var instance,
      object_params = JSON.parse($trigger.attr('data-object-params') || "{}");

  if($trigger.attr('data-object-id') === "page") {
    instance = GGRC.page_instance();
  } else {
    instance = CMS.Models.get_instance(
      $trigger.data('object-singular'),
      $trigger.attr('data-object-id')
    );
  }

  $target
  .modal_form(option, $trigger)
  .ggrc_controllers_approval_workflow({
    object_params : object_params,
    current_user : GGRC.current_user,
    instance : instance
  });
});

})(window.can, window.can.$, window.GGRC, window.CMS);


//Calendar authentication

jQuery(function($){
  $('body').on('click', '.calendar-auth', function(e) {
    var calenderAuthWin = null,
      href = window.location.origin + "/calendar_oauth_request", //"https://ggrc-dev.googleplex.com/calendar_oauth_request"
      name = "Calendar Authentication";

    if(calenderAuthWin === null || calenderAuthWin.closed){
      calenderAuthWin = window.open(href, name);
      calenderAuthWin.focus();
    }
    else{
      calenderAuthWin.focus();
    }
  });
});
