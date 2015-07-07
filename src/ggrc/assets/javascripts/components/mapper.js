/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $) {
  "use strict";
  var MapperModel = can.Map({
      type: "Program", // We set default as program
      contact: {},
      term: "",
      object: "",
      model: {},
      bindings: {},
      is_loading: false,
      is_saving: false,
      all_selected: false,
      search_only: false,
      selected: new can.List(),
      entries: new can.List(),
      relevant: new can.List(),
      types: can.compute(function () {
        var selector_list = GGRC.Mappings.get_canonical_mappings_for(GGRC.page_model.type),
            groups = {
              "all_objects": {
                name: "All Objects",
                value: "AllObject",
                plural: "allobjects",
                table_plural: "allobjects",
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
            table_plural: cms_model.table_plural,
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
          data = {};

      if ($el.attr("type")) {
        data["type"] = $el.attr("type");
      }
      if ($el.attr("join-object-id")) {
        data["join_object_id"] = $el.attr("join-object-id");
      }
      if ($el.attr("object")) {
        data["object"] = $el.attr("object");
      }
      if ($el.attr("search-only")) {
        data["search_only"] =  /true/i.test($el.attr("search-only"));
      }
      return {
        mapper: new MapperModel(data)
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
            mapping = GGRC.Mappings.get_canonical_mapping(this.scope.attr("mapper.object"), this.scope.attr("mapper.type")),
            Model = CMS.Models[mapping.model_name],
            data = {},
            deffer = [];

        // TODO: Figure what to do with context?
        data["context"] = null;
        data[mapping.object_attr] = {
          href: instance.href,
          type: instance.type,
          id: instance.id
        };

        this.scope.attr("mapper.is_saving", true);
        _.each(this.scope.attr("mapper.selected"), function (desination) {
          data[mapping.option_attr] = desination;
          var modelInstance = new Model(data);

          deffer.push(modelInstance.save());
        });
        $.when.apply($, deffer).then(function () {
          this.scope.attr("mapper.is_saving", false);
          // TODO: Find proper way to dismiss the modal
          this.element.find(".modal-dismiss").trigger("click");
        }.bind(this));
      },
      "setBinding": function () {
        if (this.scope.attr("mapper.search_only")) {
          return;
        }
        var table_plural = this.scope.attr("mapper.model.table_plural"),
            selected = CMS.Models.get_instance(this.scope.attr("mapper.object"), this.scope.attr("mapper.join_object_id")),
            binding;

        table_plural = (selected.has_binding(table_plural) ? "" : "related_") + table_plural;
        binding = selected.get_binding(table_plural);
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
        this.scope.attr("mapper.relevant", []);

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

        this.scope.attr("mapper.all_selected", selected.length === entries.length);
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
      page_loading: false,
      loading_or_saving: can.compute(function () {
        return this.attr("page_loading") || this.attr("mapper.is_saving");
      })
    },
    events: {
      "inserted":  function () {
        this.element.find(".results-wrap").cms_controllers_infinite_scroll();
        this.getResults();
      },
      ".modalSearchButton click": "getResults",
      "{scope} type": "getResults",
      "{scope} entries": "drawPage",
      ".results-wrap scrollNext": "drawPage",
      ".object-check-all change": function (el, ev) {
        var que = new RefreshQueue(),
            entries = _.map(this.scope.attr("entries"), function (entry) {
              return entry.instance;
            });

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
        if (this.scope.attr("page_loading")) {
          return;
        }
        var que = new RefreshQueue(),
            page = this.scope.attr("page"),
            next_page = page + 1,
            per_page = +this.scope.attr("items-per-page"),
            page_items = _.map(this.scope.attr("entries").slice(page * per_page, next_page * per_page), function (entry) {
              return entry.instance;
            }),
            options = this.scope.attr("options");

        if (!page_items.length) {
          return;
        }
        this.scope.attr("page_loading", true);
        que.enqueue(page_items).trigger().then(function (models) {
          this.scope.attr("page_loading", false);
          this.scope.attr("page", next_page);
          options.push.apply(options, can.map(models, function (model) {
            if (this.scope.attr("mapper.search_only")) {
              return {
                instance: model,
                selected_object: false,
                binding: {},
                mappings: []
              };
            }
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
      "searchFor": function (data) {
        data.options = data.options || {};
        var join_model = GGRC.Mappings.join_model_name_for(this.scope.attr("mapper.object"), data.model_name);

        if (join_model !== "TaskGroupObject" && data.model_name === "Program") {
          data.options.permission_parms = {
            __permission_type: "create",
            __permission_model: join_model
          };
        }
        data.options.__permission_type = data.options.__permission_type || "read";
        data.model_name = _.isString(data.model_name) ? [data.model_name] : data.model_name;

        return GGRC.Models.Search.search_for_types(data.term || "", data.model_name, data.options);
      },
      "getResults": function () {
        var model_name = this.scope.attr("type"),
            contact = this.scope.attr("contact"),
            permission_parms = {},
            search = [],
            list,
            relevant;

        this.scope.attr("page", 0);
        this.scope.attr("entries", []);
        this.scope.attr("selected", []);
        this.scope.attr("options", []);
        this.scope.attr("select_all", false);

        if (model_name === "AllObject") {
          model_name = this.scope.attr("types.all_objects.models");
        }
        if (!_.isEmpty(contact)) {
          permission_parms.contact_id = contact.id;
        }

        this.scope.attr("page_loading", true);
        relevant = _.map(this.scope.attr("mapper.relevant"), function (relevant) {
          return {
            model_name: relevant.model_name,
            term: relevant.filter.title
          };
        });
        search.push({
            term: this.scope.attr("term"),
            model_name: model_name,
            options: permission_parms
        });
        $.merge(search, relevant);
        search = _.map(search, function (query) {
          return new GGRC.ListLoaders.SearchListLoader(function (binding) {
            return this.searchFor(query).then(function (mappings) {
              return mappings.entries;
            });
          }.bind(this)).attach({});
        }.bind(this));

        list = (search.length > 1) ?
                  new GGRC.ListLoaders.IntersectingListLoader(search).attach()
                : search[0];

        list.refresh_stubs().then(function (options) {
          this.scope.attr("page_loading", false);
          this.scope.attr("entries", options);
        }.bind(this));
      }
    }
  });
  can.Component.extend({
    tag: "mapper-filter",
    template: "<content />",
    scope: {
      menu: can.compute(function () {
        var type = this.attr("type") === "AllObject" ? GGRC.page_model.type : this.attr("type"),
            mappings = GGRC.Mappings.get_canonical_mappings_for(type);
        return _.map(_.keys(mappings), function (mapping) {
          return CMS.Models[mapping];
        });
      })
    },
    events: {
      ".add-filter-rule click": function (el, ev) {
        ev.preventDefault();
        this.scope.attr("relevant").push({
          value: "",
          filter: new can.Map(),
          model_name: this.scope.attr("menu")[0].model_singular
        });
      },
      ".ui-autocomplete-input autocomplete:select": function (el, ev, data) {
        var index = el.data("index"),
            panel = this.scope.attr("relevant")[index];

        panel.attr("filter", data.item);
      },
      ".remove_filter click": function (el) {
        this.scope.attr("relevant").splice(el.data("index"), 1);
      }
    }
  });

  $("body").on("click",
  '[data-toggle="unified-mapper"], \
   [data-toggle="unified-search"]',
  function (ev) {
    ev.preventDefault();
    var btn = $(ev.currentTarget),
        data = btn.data(),
        isSearch = /unified-search/ig.test(data.toggle);

    btn.data("tooltip").hide();
    _.each(data, function (val, key) {
      data[can.camelCaseToUnderscore(key)] = val;
      delete data[key];
    });
    GGRC.Controllers.ModalSelector.launch($(this), _.extend({
      "object": btn.data("join-object-type"),
      "type": btn.data("join-option-type"),
      "join-id": btn.data("join-object-id"),
      "search-only": isSearch
    }, data));
  });
})(window.can, window.can.$);

