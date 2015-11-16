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
    scope: {
      editable: "@",
      deferred: "@",
      groups: {
        "verifier": [],
        "assignee": [],
        "requester": []
      },
    },
    events: {
    }
  });

  can.Component.extend({
    tag: "people-group",
    template: can.view(GGRC.mustache_path + "/base_templates/people_group.mustache"),
    scope: {
      limit: "@",
      mapping: "@",
      required: "@",
      type: "@",
      toggle_add: false,
      remove_role: function(parent_scope, target) {
        var person = CMS.Models.Person.findInCacheById(target.data("person"));
        var rel = function (obj) {
          return _.map(obj.related_sources.concat(obj.related_destinations), function(r) {
            return r.id;
          });
        };
        var ids = _.intersection(rel(person), rel(this.instance));
        var type = this.type;
        _.each(ids, function (id) {
          var rel = CMS.Models.Relationship.findInCacheById(id);
          if (rel.attrs && rel.attrs.AssigneeType) {
            rel.refresh().then(function (rel) {
              var roles = rel.attrs.AssigneeType.split(",");
              roles = _.filter(roles, function (role) {
                return role && (role.toLowerCase() !== type);
              });
              rel.attrs.attr("AssigneeType", roles.join(","));
              rel.save();
            });
          }
        });
      },
    },
    events: {
      ".person-selector input autocomplete:select": function (el, ev, ui) {
        var person = ui.item,
            destination = this.scope.instance,
            deferred = this.scope.deferred;

        if (deferred === "true") {
          destination.mark_for_addition("related_objects_as_destination", person, {
            attrs: {
              "AssigneeType": can.capitalize(this.scope.type),
            }
          });
        } else {
          new CMS.Models.Relationship({
            attrs: {
              "AssigneeType": can.capitalize(this.scope.type),
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
        if (this.attr("editable") === "true" && _.isNull(this.attr("limit")) ||
            +this.attr("limit") < this.attr("people").length) {
          return options.fn(options.context);
        }
        return options.inverse(options.context);
      }
    }
  });
})(window.can);
