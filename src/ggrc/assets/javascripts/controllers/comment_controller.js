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
        //init: function() {
        //    this.scope.attr("source_mapping", instance);
        //},
        "cleanPanel": function () {
            this.scope.attachments.replace([]);
            this.element.find("textarea").val("");
        },
        ".js-trigger-attachdata click": function (el, ev) {
            alert("ATTACH DATA TODO");
            this.scope.attachments.push();
        },
        ".btn-success click": function (el, ev) {
            var $textarea = this.element.find(".add-comment textarea"),
                text = $.trim($textarea.val()),
                attachments = this.scope.attachments;

            if (!text.length && !attachments.length) {
                return;
            }
            this.scope.data = {
                author: "urban",
                timestamp: "zdaj",
                comment: text,
                attachments: _.map(attachments, function (attachment) {
                    return attachment;
                })
            };
            this.cleanPanel();
        }
    }
});
