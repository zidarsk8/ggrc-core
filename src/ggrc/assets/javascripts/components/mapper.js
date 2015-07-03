/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $) {
  "use strict";
  var MapperModel = can.Map({
      type: "",
      contact: {},
      term: "",
      model: {},
      bindings: {},
      isLoading: false,
      allSelected: false,
      selected: new can.List(),
      entries: new can.List(),
      types: can.compute(function () {
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
      })
    });


  can.Component.extend({
    tag: "modal-mapper",
    template: "<content />",
    scope: function (attrs, parentScope, el) {
      var $el = $(el),
          mapperInst = new MapperModel({
            type: $el.attr("type"),
            join_object_id: $el.attr("join-object-id"),
            object: $el.attr("object"),
          });
      return {
        mapper: mapperInst
      };
    },
    events: {
      "inserted": function () {
        this.setModel();
        this.setBinding();
      },
      ".modal-footer .btn-map click": function (el, ev) {
        ev.preventDefault();
        if (el.hasClass("disabled")) {
          return;
        }
        var instance = GGRC.page_instance(),
            data = {},
            deffer = [];

        data["context"] = null;
        data["source"] = {
          href: instance.href,
          type: instance.type,
          id: instance.id
        };
        this.scope.attr("isLoading", true);
        _.each(this.scope.attr("mapper.selected"), function (desination) {
          data["destination"] = desination;
          var model = new CMS.Models.Relationship(data);

          deffer.push(model.save());
        });
        $.when.apply($, deffer).then(function () {
          this.scope.attr("isLoading", false);
          // TODO: Find proper way to dismiss the modal
          this.element.find(".modal-dismiss").trigger("click");
        }.bind(this));
      },
      "setBinding": function () {
        var model_name = this.scope.attr("mapper.model.plural").toLowerCase(),
            selected = CMS.Models.get_instance(this.scope.attr("mapper.object"), this.scope.attr("mapper.join_object_id")),
            binding;

        model_name = (selected.has_binding(model_name) ? "" : "related_") + model_name;
        binding = selected.get_binding(model_name);
        binding.refresh_list().then(function (mappings) {
          can.each(mappings, function (mapping) {
            this.scope.attr("mapper.bindings")[mapping.instance.id] = mapping;
          }, this);
        }.bind(this));
      },
      "setModel": function () {
        var type = this.scope.attr("mapper.type"),
            types = this.scope.attr("mapper.types");
        if (type === "AllObject") {
          return this.scope.attr("mapper.model", types["all_objects"]);
        }
        types = _.reduce(_.values(types), function (memo, val) {
          if (val.items) {
            return memo.concat(val.items);
          }
          return memo;
        }, []);
        this.scope.attr("mapper.model", _.findWhere(types, {value: type}));
      },
      "{mapper.type} change": function () {
        this.scope.attr("mapper.term", "");
        this.scope.attr("mapper.contact", {});
        this.setModel();
        this.setBinding();
      },
      "#search-by-owner autocomplete:select": function (el, ev, data) {
        this.scope.attr("mapper.contact", data.item);
      },
      "#search-by-owner keyup": function (el, ev) {
        if (!el.val()) {
          this.scope.attr("mapper.contact", {});
        }
      },
      "allSelected": function () {
        var selected = this.scope.attr("mapper.selected"),
            entries = this.scope.attr("mapper.entries");

        this.scope.attr("mapper.allSelected", selected.length === entries.length);
      },
      "{mapper.entries} length": "allSelected",
      "{mapper.selected} length": "allSelected"
    }
  });
  can.Component.extend({
    tag: "mapper-results",
    template: "<content />",
    scope: {
      "items-per-page": "@",
      page: 0,
      options: new can.List(),
      select_all: false,
      pageLoading: false
    },
    events: {
      "inserted":  function () {
        this.element.find(".results-wrap").cms_controllers_infinite_scroll();
        this.getResults();
      },
      ".modalSearchButton click": "getResults",
      "{scope} type": "getResults",
      ".results-wrap scrollNext": "drawPage",
      ".tree-item .openclose click": function (el, ev) {
        ev.preventDefault();
        el.openclose();
      },
      ".object-check-all change": function (el, ev) {
        var que = new RefreshQueue(),
            entries = this.scope.attr("entries");

        this.scope.attr("select_all", true);
        this.scope.attr("isloading", true);
        que.enqueue(entries).trigger().then(function (models) {
          this.scope.attr("isloading", false);
          this.scope.attr("selected", _.map(models, function (model) {
            return {
              id: model.id,
              type: model.type,
              href: model.href
            };
          }));
        }.bind(this));
      },
      ".tree-item .object-check-single change": function (el, ev) {
        if (el.hasClass("disabled")) {
          return;
        }

        var uid = el.closest(".tree-item").data("id"),
            isChecked = el.prop("checked"),
            item = _.find(this.scope.attr("options"), function (option) {
                return option.instance.id === uid;
              }),
            selected = this.scope.attr("selected"),
            needle = {id: item.instance.id},
            index;

        if (!_.findWhere(selected, needle)) {
          selected.push({
            id: item.instance.id,
            type: item.instance.type,
            href: item.instance.href
          });
        } else {
          index = _.findIndex(selected, needle);
          selected.splice(index, 1);
        }
      },
      "drawPage": function () {
        if (this.scope.attr("pageLoading") || this.scope.attr("lastPage")) {
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
        this.scope.attr("pageLoading", true);
        que.enqueue(page_items).trigger().then(function (models) {
          this.scope.attr("pageLoading", false);
          this.scope.attr("page", next_page);
          options.push.apply(options, can.map(models, function (model) {
            var selected = CMS.Models.get_instance(this.scope.attr("mapper.object"), this.scope.attr("mapper.join_object_id")),
                binding = selected.get_binding(this.scope.attr("mapper.model.plural").toLowerCase()),
                bindings = this.scope.attr("mapper.bindings");

            if (bindings[model.id]) {
              return _.extend(bindings[model.id], {
                selected_object: selected
              });
            }
            return {
              instance: model,
              selected_object: selected,
              binding: binding,
              mappings: []
            };
          }.bind(this)));
        }.bind(this));
      },
      "getResults": function () {
        var model_name = this.scope.attr("type"),
            contact = this.scope.attr("contact"),
            join_model = GGRC.Mappings.join_model_name_for(CMS.Models[model_name], model_name),
            permission_parms = {
              __permission_type: "read"
            };

        this.scope.attr("page", 0);
        this.scope.attr("entries", []);
        this.scope.attr("selected", []);
        this.scope.attr("options", []);
        this.scope.attr("select_all", false);

        if (join_model !== "TaskGroupObject" && model_name === "Program") {
          permission_parms = {
            __permission_type: "create",
            __permission_model: join_model
          };
        }
        if (model_name === "AllObject") {
          model_name = this.scope.attr("types.all_objects.models");
        }
        if (contact) {
          permission_parms.contact_id = contact.id;
        }

        this.scope.attr("pageLoading", true);
        model_name = _.isString(model_name) ? [model_name] : model_name;
        GGRC.Models.Search
          .search_for_types(this.scope.attr("term") || "", model_name, permission_parms)
          .then(function (response) {
            var entries = _.flatten(_.map(model_name, function (name) {
                            return response.getResultsForType(name);
                          }));

            this.scope.attr("entries", entries);
            this.scope.attr("pageLoading", false);
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


  $("body").on("click",
  '[data-toggle="modal-selector"], \
   [data-toggle="modal-relationship-selector"], \
   [data-toggle="multitype-object-modal-selector"], \
   [data-toggle="multitype-multiselect-modal-selector"], \
   [data-toggle="multitype-modal-selector"]',
  function (ev) {
    ev.preventDefault();
    var btn = $(ev.currentTarget),
        data = btn.data();

    _.each(data, function (val, key) {
      data[can.camelCaseToUnderscore(key)] = val;
      delete data[key];
    });
    GGRC.Controllers.ModalSelector.launch($(this), _.extend({
      "object": btn.data("join-object-type"),
      "type": btn.data("join-option-type"),
      "join-id": btn.data("join-object-id")
    }, data));
  });
})(window.can, window.can.$);

