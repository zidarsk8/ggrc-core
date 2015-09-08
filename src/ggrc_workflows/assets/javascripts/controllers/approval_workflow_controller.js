/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/

;(function(can, $, GGRC, CMS) {

GGRC.Controllers.Modals("GGRC.Controllers.ApprovalWorkflow", {
  defaults : {
    original_object : null,
    new_object_form: true,
    model: CMS.ModelHelpers.ApprovalWorkflow,
    modal_title: "Submit for review",
    custom_save_button_text: "Submit",
    content_view: GGRC.mustache_path + "/wf_objects/approval_modal_content.mustache",
    button_view : GGRC.Controllers.Modals.BUTTON_VIEW_SAVE_CANCEL
  }
}, {
  init : function() {
    this.options.button_view = GGRC.Controllers.Modals.BUTTON_VIEW_SAVE_CANCEL;
    this._super.apply(this, arguments);
    this.options.attr("instance", new CMS.ModelHelpers.ApprovalWorkflow({
      original_object : this.options.instance
    }));
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

})(this.can, this.can.$, this.GGRC, this.CMS);


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
