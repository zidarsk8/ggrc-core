/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $) {
  "use strict";
  var MapperModel = can.Map({
      type: "AllObject", // We set default as All Object
      contact: {},
      deferred: "@",
      deferred_to: "@",
      term: "",
      object: "",
      model: {},
      bindings: {},
      is_loading: false,
      is_saving: false,
      all_selected: false,
      search_only: false,
      join_object_id: "",
      selected: new can.List(),
      entries: new can.List(),
      relevant: new can.List(),
      model_from_type: function (type) {
        var types = _.reduce(_.values(this.types()), function (memo, val) {
          if (val.items) {
            return memo.concat(val.items);
          }
          return memo;
        }, []);
        return _.findWhere(types, {value: type});
      },
      types: can.compute(function () {
        var selector_list = GGRC.Mappings.get_canonical_mappings_for(this.object),
            forbidden = ["workflow", "taskgroup", "gdrivefolder", "context"],
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
          if (!model_name || !CMS.Models[model_name] || ~forbidden.indexOf(model_name.toLowerCase())) {
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
    template: can.view(GGRC.mustache_path + "/modals/mapper/base.mustache"),
    scope: function (attrs, parentScope, el) {
      var $el = $(el),
          data = {},
          id = +$el.attr("join-object-id"),
          object = $el.attr("object");

      if ($el.attr("search-only")) {
        data["search_only"] =  /true/i.test($el.attr("search-only"));
      }
      if (object) {
        data["object"] = object;
      }
      if (!data["search_only"]) {
        data["type"] = id === GGRC.page_instance().id ?
                       $el.attr("type")
                       : GGRC.tree_view.sub_tree_for[object].display_list[0];
      }
      data["join_object_id"] = id || GGRC.page_instance().id;
      return {
        mapper: new MapperModel(data)
      };
    },
    events: {
      "inserted": function () {
        this.setModel();
        this.setBinding();
      },
      "defferedSave": function () {
        var data = {
              multi_map: true,
              arr: _.map(this.scope.attr("mapper.selected"), function (desination) {
                    var inst = _.find(this.scope.attr("mapper.entries"), function (entry) {
                      return entry.instance.id === desination.id;
                    });
                    if (inst) {
                      return inst.instance;
                    }
                  }.bind(this))
            };
        this.scope.attr("deferred_to").controller.element.trigger("deffer:add", [data, {map_and_save: true}]);
        // TODO: Find proper way to dismiss the modal
        this.element.find(".modal-dismiss").trigger("click");
      },
      ".modal-footer .btn-map click": function (el, ev) {
        ev.preventDefault();
        if (el.hasClass("disabled")) {
          return;
        }
        // TODO: Figure out nicer / proper way to handle deferred save
        if (this.scope.attr("deferred")) {
          return this.defferedSave();
        }
        var type = this.scope.attr("mapper.type"),
            object = this.scope.attr("mapper.object"),
            instance = CMS.Models[object].findInCacheById(this.scope.attr("mapper.join_object_id")),
            mapping = GGRC.Mappings.get_canonical_mapping(this.scope.attr("mapper.object"), type),
            Model = CMS.Models[mapping.model_name],
            data = {},
            deffer = [],
            que = new RefreshQueue();

        this.scope.attr("mapper.is_saving", true);
        que.enqueue(instance).trigger().done(function (inst) {
          // TODO: Figure what to do with context?
          data["context"] = null;
          data[mapping.object_attr] = {
            href: instance.href,
            type: instance.type,
            id: instance.id
          };

          _.each(this.scope.attr("mapper.selected"), function (desination) {
            var modelInstance;
            data[mapping.option_attr] = desination;
            modelInstance = new Model(data);
            deffer.push(modelInstance.save());
          }, this);

          $.when.apply($, deffer)
            .fail(function (response, message) {
              $("body").trigger("ajax:flash", {"error": message});
            }.bind(this))
            .always(function () {
              this.scope.attr("mapper.is_saving", false);
              // TODO: Find proper way to dismiss the modal
              this.element.find(".modal-dismiss").trigger("click");
            }.bind(this));
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
        if (!selected.has_binding(table_plural)) {
          return;
        }
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

        if (~["All Object", "AllObject"].indexOf(type)) {
          return this.scope.attr("mapper.model", types["all_objects"]);
        }
        this.scope.attr("mapper.model", this.scope.mapper.model_from_type(type));
      },
      "{mapper} type": function () {
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
            page_items = this.scope.attr("entries").slice(page * per_page, next_page * per_page),
            options = this.scope.attr("options");

        if (!page_items.length) {
          return;
        }

        que.enqueue(_.pluck(page_items, "instance")).trigger().then(function (models) {
          this.scope.attr("page_loading", false);
          this.scope.attr("page", next_page);
          options.push.apply(options, can.map(models, function (model) {
            if (!model.type) {
              return;
            }
            if (this.scope.attr("mapper.search_only")) {
              return {
                instance: model,
                selected_object: false,
                binding: {},
                mappings: []
              };
            }
            var selected = CMS.Models.get_instance(this.scope.attr("mapper.object"), this.scope.attr("mapper.join_object_id")),
                mapper = this.scope.mapper.model_from_type(model.type),
                binding, bindings = this.scope.attr("mapper.bindings");

            if (bindings[model.id]) {
              return _.extend(bindings[model.id], {
                selected_object: selected
              });
            }
            if (selected.has_binding(mapper.plural.toLowerCase())) {
              binding = selected.get_binding(mapper.plural.toLowerCase());
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


  $("body").on("click",
  '[data-toggle="unified-mapper"], \
   [data-toggle="unified-search"]',
  function (ev) {
    ev.preventDefault();
    var btn = $(ev.currentTarget),
        data = {},
        isSearch;

    _.each(btn.data(), function (val, key) {
      data[can.camelCaseToUnderscore(key)] = val;
    });

    if (data.tooltip) {
      data.tooltip.hide();
    }
    isSearch = /unified-search/ig.test(data.toggle);
    GGRC.Controllers.MapperModal.launch($(this), _.extend({
      "object": btn.data("join-object-type"),
      "type": btn.data("join-option-type"),
      "join-object-id": btn.data("join-object-id"),
      "search-only": isSearch
    }, data));
  });
})(window.can, window.can.$);

