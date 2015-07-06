/*!
  Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: ivan@reciprocitylabs.com
  Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $) {
  var url = can.route.deparam(window.location.search.substr(1)),
      filterModel = can.Map({
        model_name: "Program",
        value: "",
        filter: {}
      }),
      panelModel = can.Map({
        selected: {},
        models: null,
        type: "Program",
        filter: "",
        relevance: can.compute(function () {
          return new can.List();
        }),
        columns: function () {
          return CMS.Models[this.attr("type")].tree_view_options.attr_list;
        }
      }),
      panelsModel = can.Map({
        items: new can.List()
      }),
      exportModel = can.Map({
        panels: new panelsModel(),
        url: "/_service/export_csv",
        type: url.model_type || "Program",
        edit_filename: false,
        only_relevant: false,
        filename: "Export Objects",
        get_filename: can.compute(function () {
          return this.attr("filename").replace(/\s+/, "_").toLowerCase() + ".csv";
        }),
        data_grid: function () {
          return _.has(url, "data_grid");
        }
      });

  can.Component.extend({
    tag: "csv-export",
    template: "<content></content>",
    scope: function () {
      return {
        export: new exportModel()
      };
    },
    events: {
      ".btn-title-change click": function (el, ev) {
        ev.preventDefault();
        this.scope.attr("export.edit_filename", !this.scope.attr("export.edit_filename"));
      },
      ".save-template .btn-success click": function (el, ev) {
        ev.preventDefault();
        var panels = this.scope.attr("export.panels.items");
        query = _.map(panels, function (panel, index) {
          var relevant_filter = _.reduce(panel.relevance(),  function(query, el){
                return (query && query+" AND ")+"#"+el.model_name+","+el.filter.id+"#";
              }, "")
          return {
            object_name: panel.type,
            fields: _.compact(_.map(Object.keys(panel.selected), function (key) {
              return panel.selected[key] === true ? key : null;
            })),
            filters: GGRC.query_parser.join_queries(
              GGRC.query_parser.parse(relevant_filter || ""),
              GGRC.query_parser.parse(panel.filter || "")
            )
          };
        });

        GGRC.Utils.ajax({
          type: "POST",
          url: this.scope.attr("export.url"),
          data: query
        }).then(function (data) {
          GGRC.Utils.download(this.scope.attr("export.get_filename"), data);
        }.bind(this))
        .fail(function (data) {
          $("body").trigger("ajax:flash", {"error": data});
        }.bind(this));
      }
    }
  });


  can.Component.extend({
    tag: "export-group",
    template: "<content></content>",
    scope: {
      _index: 0
    },
    events: {
      "inserted": function () {
        this.addPanel({
          type: url.model_type || "Program"
        });
      },
      addPanel: function (data) {
        data = data || {};
        var index = this.scope.attr("_index") + 1;
        if (!data.type) {
          data.type = "Program";
        }

        this.scope.attr("_index", index);
        data.index = index;
        return this.scope.attr("panels.items").push(new panelModel(data));
      },
      getIndex: function (el) {
        return +el.closest("export-panel").control().scope.attr("item.index");
      },
      ".remove_filter_group click": function (el, ev) {
        ev.preventDefault();
        var elIndex = this.getIndex(el),
            index = _.pluck(this.scope.attr("panels.items"), "index").indexOf(elIndex);
        this.scope.attr("panels.items").splice(index, 1);
      },
      "#addAnotherObjectType click": function (el, ev) {
        ev.preventDefault();
        this.addPanel();
      }
    }
  });

  can.Component.extend({
    tag: "export-panel",
    template: "<content></content>",
    scope: {
      panel_number: "@"
    },
    helpers: {
      first_panel: function (options) {
        if (+this.attr("panel_number") > 0) {
          return options.fn();
        }
        return options.inverse();
      }
    }
  });

  can.Component.extend({
    tag: "csv-relevance-filter",
    template: "<content />",
    scope: {
      index: "@",
      menu: can.compute(function () {
        var type = this.attr("type"),
            mappings = GGRC.Mappings.get_canonical_mappings_for(type);
        return _.map(_.keys(mappings), function (mapping) {
          return CMS.Models[mapping];
        });
      })
    },
    events: {
      "inserted": function (el, ev) {
        var index = +this.scope.attr("panel_number");

        // TODO: This could be probably written nicer e.g. pass parametars in template?
        if (index === 0 && url.relevant_id && url.relevant_type) {
          var dfd = this.searchByType(url.relevant_id, url.relevant_type),
              que = new RefreshQueue();

          dfd.then(function (response) {
            var result = response.getResultsFor(url.relevant_type)[0];
            que.enqueue(result).trigger().then(function (item) {
              this.scope.attr("relevance").push(new filterModel({
                model_name: url.relevant_type,
                value: url.relevant_id,
                filter: result
              }));
            }.bind(this));
          }.bind(this));
        }
      },
      "searchByType": function (id, type) {
        return GGRC.Models.Search.search_for_types(id, [type]);
      },
      ".add-filter-rule click": function (el, ev) {
        ev.preventDefault();
        this.scope.attr("relevance").push(new filterModel({
          value: "",
          filter: new can.Map(),
          model_name: this.scope.attr("menu")[0].model_singular
        }));
      },
      ".ui-autocomplete-input autocomplete:select": function (el, ev, data) {
        var index = el.data("index"),
            panel = this.scope.attr("relevance")[index];

        panel.attr("filter", data.item);
      },
      ".remove_filter click": function (el) {
        this.scope.attr("relevance").splice(el.data("index"), 1);
      }
    }
  });

  $("#csv_export").html(can.view(GGRC.mustache_path +
                                 "/import_export/export.mustache", {}));
})(window.can, window.can.$);
