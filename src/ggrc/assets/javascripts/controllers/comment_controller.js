/*!
 Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: urban@reciprocitylabs.com
 Maintained By: urban@reciprocitylabs.com
 */

can.Component.extend({
  tag: "add-comment",
  template: can.view("/static/mustache/base_templates/add_comment.mustache"),
  scope: {
    attachments: new can.List(),
    parent_instance: null,
    instance: null,
    instance_attr: "@",
    source_mapping: "@",
    source_mapping_source: "@",
    mapping: "@",
    deferred: "@",
    attributes: {},
    list: [],
    // the following are just for the case when we have no object to start with,
    changes: []

  },
  events: {
    init: function() {
      this.scope.attr("source_mapping", GGRC.page_instance());
    },
    "cleanPanel": function () {
      this.scope.attachments.replace([]);
      this.element.find("textarea").val("");
    },
    ".js-trigger-attachdata click": function (el, ev) {
      //this.scope.attachments.push();
      console.log("WIP")
    },
    ".btn-success click": function (el, ev) {
      var $textarea = this.element.find(".add-comment textarea"),
        description = $.trim($textarea.val()),
        attachments = this.scope.attachments,
        source = this.scope.source_mapping,
        comment = CMS.Models.Comment;

      if (!description.length && !attachments.length) {
        return;
      }
      var data = {
        description: description,
        context: source.context
      };
      new comment(data).save();
      this.cleanPanel();
    }
  }
});

(function(can, $) {

can.Control("GGRC.Controllers.Comments", {

}, {
  _create_relationship: function(source, destination) {

    if (!destination) {
      return $.Deferred().resolve();
    }

    return new CMS.Models.Relationship({
      source: source.stub(),
      destination: destination,
      context: source.context,
    }).save();
  },
  "{CMS.Models.Comment} created": function(model, ev, instance) {
    if (!(instance instanceof  CMS.Models.Comment)) {
      return;
    }
    var parent_dfd = this._create_relationship(GGRC.page_instance(), instance);
    instance.delay_resolving_save_until($.when(parent_dfd));
  }
});

  $(function() {
    $(document.body).ggrc_controllers_comments();
  });

})(this.can, this.can.$);
