/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $) {
  "use strict";

  can.Component.extend({
    tag: "modal-mapper",
    template: "<content />",
    scope: {
      object: "@",
      type: "@"
    },
    events: {
      "mapper-selector onTypeChange": function (el, ev, data) {
        this.scope.attr("type", data.value);
      }
    }
  });
  can.Component.extend({
    tag: "mapper-create-new",
    template: "<content />",
    events: {
      "{document} onTypeChange": function (el, ev, data) {
        this.scope.attr(data);
      }
    }
  });
  can.Component.extend({
    tag: "mapper-filter",
    template: "<content />",
    scope: {
      panels: [],
      menu: can.map(
            Array.prototype.concat.call([],
              "Program Regulation Policy Standard Contract Clause Section Objective Control".split(" "),
              "Person System Process DataAsset Product Project Facility Market".split(" ")
            ), function (key) {
              return CMS.Models[key];
            })
    },
    events: {
      ".add-filter-rule click": function (el, ev) {
        ev.preventDefault();
        this.scope.panels.push({
          value: "",
          model_name: this.scope.menu[0].model_singular
        });
      },
      ".remove_filter click": function(el) {
        var index = el.data("index");
        this.scope.panels.splice(index, 1);
      }
    }
  });
  can.Component.extend({
    tag: "mapper-selector",
    template: "<content />",
    scope: {
      type: "@",
      groups: function (attrs) {
        var selector_list = GGRC.Mappings.get_canonical_mappings_for(GGRC.page_model.type),
            groups = {
              "all_objects": {
                name: "All Objects",
                value: "AllObject",
                plural: "allobjects",
                singular: "AllObject"
              },
              "entities": {
                name: "People/Groups",
                items: []
              },
              "business": {
                name: "Assets/Business",
                items: []
              },
              "governance": {
                name: "Governance",
                items: []
              }
            };
        can.each(selector_list, function (model, model_name) {
          if (!model_name || ~["workflow"].indexOf(model_name.toLowerCase())) {
            return;
          }
          var cms_model = CMS.Models[model_name],
              join_model = GGRC.ModalOptionDescriptor.from_join_model(model.model_name, model.option_attr, model_name),
              group = !groups[cms_model.category] ? "governance" : cms_model.category;


          groups[group]["items"].push({
            value: cms_model.shortName,
            label: cms_model.title_plural,
            singular: cms_model.shortName,
            plural: cms_model.title_plural.toLowerCase().replace(/\s+/, "_"),
            isSelected: cms_model.shortName === attrs.type
          });
        }, this);

        return groups;
      }
    },
    events: {
      "onTypeChange": function () {
        var selected = this.element.find(":selected"),
            data = {
              name: selected.attr("label"),
              value: selected.val(),
              singular: selected.data("singular"),
              plural: selected.data("plural")
            };
        console.log("onTypeChange", data);
        this.element.trigger("onTypeChange", data);
      },
      "select change": "onTypeChange",
      "inserted":  "onTypeChange"
    }
  });

  $("body").on("click",
  "[data-toggle='modal-selector'], \
   [data-toggle='modal-relationship-selector'], \
   [data-toggle='multitype-object-modal-selector'], \
   [data-toggle='multitype-multiselect-modal-selector'], \
   [data-toggle='multitype-modal-selector']",
  function (ev) {
    ev.preventDefault();
    var btn = $(ev.currentTarget);

    GGRC.Controllers.ModalSelector.launch($(this), {
      "object": btn.data("join-object-type"),
      "type": btn.data("join-option-type"),
      "join-id": btn.data("join-object-id")
    });
  });
})(window.can, window.can.$);
