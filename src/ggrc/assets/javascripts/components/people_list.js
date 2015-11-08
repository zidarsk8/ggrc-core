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
        },
        deferred: {
          type: "boolean"
        }
      },
      editable: "@",
      deferred: "@",
      groups: {
        "verifier": [],
        "assignee": [],
        "requester": []
      }
    },
    events: {
    }
  });

  can.Component.extend({
    tag: "people-group",
    template: can.view(GGRC.mustache_path + "/base_templates/people_group.mustache"),
    viewModel: {
      define: {
        required: {
          type: "boolean"
        },
        limit: {
          type: "number"
        }
      },
      limit: "@",
      mapping: "@",
      required: "@",
      type: "@",
      toggle_add: false,
    },
    events: {
      ".person-selector input autocomplete:select": function (el, ev, ui) {
        var person = ui.item,
            destination = this.viewModel.instance,
            deferred = this.viewModel.deferred;
        if (deferred) {
          destination.mark_for_addition("related_objects_as_destination", person, {
            attrs: {
              "AssigneeType": can.capitalize(this.viewModel.type),
            }
          });
        } else {
          new CMS.Models.Relationship({
            attrs: {
              "AssigneeType": can.capitalize(this.viewModel.type),
            },
            source: {
              href: person.href,
              type: person.type,
              id: person.id
            },
            context: {},
            destination: {
              href: destination.href,
              type: destination.type,
              id: destination.id
            }
          }).save();
        }
      },
    },
    helpers: {
      show_add: function (options) {
        if (this.attr("editable")) {
          if (_.isNull(this.attr("limit")) ||
              this.attr("limit") > this.attr("people").filter(function (person) {
                return person.attr("person_state") !== "deleted";
              }).length) {
            return options.fn();
          }
        }
        return options.inverse();
      }
    }
  });
})(window.can);
