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
      type: "@",
      selected: new can.List(),
      selected_all: false,
      owner: {},
      term: "",
      person: "",
      "join-object-id": "@"
    },
    events: {
      ".modalSearchButton click": function (el, ev) {
        ev.preventDefault();
        var results = this.element.find("mapper-results").control();
        results.getResults(this.scope.attr("term"), this.scope.attr("owner"));
      },
      "#search-by-owner autocomplete:select": function (el, ev, data) {
        this.scope.attr("owner", data.item);
      },
      "mapper-selector onTypeChange": function (el, ev, data) {
        this.scope.attr("type", data.value);
      },
      "mapper-results onSelect": function (el, ev, count) {
        this.scope.attr("selected_all", count === this.scope.attr("selected").length);
      },
      "mapper-results onSelectAll": function (el, ev, ids) {
        this.scope.attr("selected").attr(ids);
      },
      "mapper-results onSelectChange": function (el, ev, select) {
        var id = select.data("id"),
            isChecked = select.prop("checked"),
            selected = this.scope.attr("selected");
        if (!~selected.indexOf(id)) {
          selected.push(id);
        } else {
          selected.splice(selected.indexOf(id), 1);
        }
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
    tag: "mapper-results",
    template: "<content />",
    scope: {
      "join-object-id": "@",
      "items-per-page": "@",
      page: 0,
      options: new can.List(),
      entries: [],
      isLoading: false
    },
    events: {
      "inserted":  function () {
        this.element.find(".results-wrap").cms_controllers_infinite_scroll();
      },
      "{document} onSelectChange": "onSelect",
      "{document} onSelectAll": "onSelect",
      "onSelect": function () {
        this.element.trigger("onSelect", this.scope.attr("entries").length);
      },
      ".results-wrap scrollNext": "drawPage",
      "{document} onTypeChange": function (el, ev, data) {
        this.scope.attr("data", data);
        this.scope.attr("name", data.value);
        this.getResults();
      },
      ".tree-item .openclose click": function (el, ev) {
        ev.preventDefault();
        el.openclose();
      },
      ".object-check-all change": function (el, ev) {
        can.each(this.scope.attr("options"), function (model) {
          model.attr("selected", true);
        });
        this.element.trigger("onSelectAll", [_.pluck(this.scope.attr("entries"), "id")]);
      },
      ".tree-item .object-check-single change": function (el, ev) {
        var uid = el.closest(".tree-item").data("id"),
            isChecked = el.prop("checked", isChecked),
            item = _.findWhere(this.scope.attr("options"), {id: uid});

        this.element.trigger.apply(this.element, ["onSelectChange"].concat(arguments));
      },
      "drawPage": function () {
        if (this.scope.attr("isLoading") || this.scope.attr("lastPage")) {
          return;
        }
        var que = new RefreshQueue(),
            page = this.scope.attr("page"),
            next_page = page + 1,
            per_page = +this.scope.attr("items-per-page"),
            page_items = this.scope.attr("entries").slice(page * per_page, next_page * per_page),
            options = this.scope.attr("options");

        if (!page_items.length) {
          return;
        }
        this.scope.attr("isLoading", true);
        que.enqueue(page_items).trigger().then(function (models) {
          this.scope.attr("isLoading", false);
          this.scope.attr("page", next_page);
          options.push.apply(options, can.map(models, function (model) {
            return {
              instance: model,
              selected_object: CMS.Models[this.scope.attr("name")],
              selected: false,
              binding: null,
              mappings: []
            };
          }.bind(this)));
        }.bind(this));
      },
      "getResults": function (term, owner) {
        var model_name = this.scope.attr("name"),
            join_model = GGRC.Mappings.join_model_name_for(CMS.Models[model_name], model_name),
            permission_parms = {
              __permission_type: "read"
            };

        this.scope.attr("page", 0);
        this.scope.attr("entries", []);
        this.scope.attr("options", []);
        if (join_model !== "TaskGroupObject" && model_name === "Program") {
          permission_parms = {
            __permission_type: "create",
            __permission_model: join_model
          };
        }
        if (model_name === "AllObject") {
          model_name = this.scope.attr("data").models;
        }
        if (owner) {
          permission_parms.contact_id = owner.id;
        }
        this.scope.attr("isLoading", true);
        model_name = _.isString(model_name) ? [model_name] : model_name;
        GGRC.Models.Search
          .search_for_types(term || "", model_name, permission_parms)
          .then(function (response) {
            var entries = _.flatten(_.map(model_name, function (name) {
                            return response.getResultsForType(name);
                          }));

            this.scope.attr("entries", entries);
            this.scope.attr("isLoading", false);
            this.drawPage();
          }.bind(this));
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
          filter: new can.Map(),
          model_name: this.scope.menu[0].model_singular
        });
      },
      ".ui-autocomplete-input autocomplete:select": function (el, ev, data) {
        var index = el.data("index"),
            panel = this.scope.attr("panels")[index];

        panel.attr("filter", data.item);
      },
      ".remove_filter click": function (el) {
        this.scope.panels.splice(el.data("index"), 1);
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
                singular: "AllObject",
                models: []
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
            name: cms_model.title_plural,
            value: cms_model.shortName,
            singular: cms_model.shortName,
            plural: cms_model.title_plural.toLowerCase().replace(/\s+/, "_"),
            isSelected: cms_model.shortName === this.type
          });
          groups["all_objects"]["models"].push(cms_model.shortName);
        }, this);
        return groups;
      }
    },
    events: {
      "onTypeChange": function () {
        var selected = this.element.find(":selected"),
            value = selected.val(),
            groups = this.scope.groups(),
            data = _.reduce(_.values(groups), function (memo, val) {
                    return _.findWhere(val.items || val, {value: value}) || memo;
                  });
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
