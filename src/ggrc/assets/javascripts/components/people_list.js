/*!
  Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: andraz@reciprocitylabs.com
  Maintained By: andraz@reciprocitylabs.com
*/

(function (can) {
  can.Component.extend({
    tag: "people-list",
    template: can.view(GGRC.mustache_path + "/base_templates/people_list.mustache"),
    viewModel: {
      define: {
        editable: {
          type: "boolean"
        }
      },
      editable: "@",
      groups: {
        "verifier": [],
        "assignee": [],
        "requester": []
      }
    },
    events: {
      inserted: function () {
        this.scope.instance.get_assignees().then(function (assignees) {

        }.bind(this));
      }
    }
  });

  can.Component.extend({
    tag: "people-group",
    template: can.view(GGRC.mustache_path + "/base_templates/people_group.mustache"),
    viewModel: {
      type: "@"
    },
    events: {
      ".person-selector input autocomplete:select": function (el, ev, ui) {
        if (_.findWhere(this.viewModel.attr("people"), {id: ui.item.id})) {
          return;
        }
        this.viewModel.attr("people").push(ui.item);
      }
    }
  });
})(window.can);
