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
          console.log("Assignees", arguments);
        }.bind(this));
      },
      ".trigger-save-yo click": function () {
        var instance = this.viewModel.attr("instance"),
            destination, relationships = [];

        // model = new CMS.Models.Relationship({
        //   attrs: {
        //     "AssigneeType": type
        //   },
        //   source: source,
        //   destination: destination
        // });
        destination = {
          context_id: instance.context_id,
          href: instance.href,
          type: instance.type,
          id: instance.id
        };
        this.viewModel.attr("groups").each(function (group, type) {
          group.each(function (person) {
            var model = new CMS.Models.Relationship({
              attrs: {
                "AssigneeType": can.capitalize(type)
              },
              source: {
                context_id: null,
                href: person.href,
                type: person.type,
                id: person.id
              },
              destination: destination
            });
            relationships.push(model.save());
          });
        });

        $.when.apply($, relationships)
            .fail(function (response, message) {

            }.bind(this))
            .always(function () {
              console.log("SUCCESS", arguments);
            });
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
