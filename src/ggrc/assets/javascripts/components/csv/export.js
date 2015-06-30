/*!
  Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: ivan@reciprocitylabs.com
  Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $) {
  var url = can.route.deparam(window.location.href.split("?")[1]),
      exportModel = can.Map({
        index: 0,
        type: url.type || "Program",
        selected: {},
        columns: function () {
          return CMS.Models[this.attr("type")].tree_view_options.attr_list;
        }
      });


  can.Component.extend({
    tag: "csv-export",
    template: "<content></content>",
    scope: {
      url: "/_service/export_csv",
      editFilename: false,
      only_relevant: false,
      filename: function () {
        return "Export Objects";
      },
      data_grid: function () {
        return _.has(url, "data_grid");
      }
    },
    events: {
      ".save-template .btn-success click": function (el, ev) {
        ev.preventDefault();
        var control = this.element.find("export-type").control();
        console.log("YO!", this, control.scope.attr("_panels"));
      }
    }
  });


  can.Component.extend({
    tag: "export-type",
    template: "<content></content>",
    scope: {
      _index: 0,
      _panels: [],
      panels: function () {
        if (!this._panels.length) {
          this._panels.push(new exportModel());
        }
        return this._panels;
      }
    },
    events: {
      getIndex: function (el) {
        return +el.closest("export-panel").attr("index");
      },
      addPanel: function (data) {
        data = data || {};
        var index = this.scope.attr("_index") + 1;
        if (!data.type) {
          data.type = "Program";
        }

        this.scope.attr("_index", index);
        data.index = index;
        return this.scope.attr("_panels").push(new exportModel(data));
      },
      ".remove_filter_group click": function (el, ev) {
        ev.preventDefault();
        var index = this.getIndex(el);
        this.scope.attr("_panels").splice(index, 1);
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
    scope: function(attrs, parentScope, el) {
      return _.find(parentScope.attr("_panels"), function (panel) {
        return panel.index === +$(el).attr("index");
      });
    },
    events: {

    },
    helpers: {
      first_panel: function (options) {
        if (+this.attr("index") > 0) {
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
      filters: [],
      data_grid: "@",
      index: "@",
      menu: can.map(["Program", "Regulation", "Policy", "Standard", "Contract",
                    "Clause", "Section", "Objective", "Control", "Person",
                    "System", "Process", "DataAsset", "Product", "Project",
                    "Facility", "Market"],
                    function (key) {
                      return CMS.Models[key];
                    })
    },
    events: {
      "inserted": function (el, ev) {
        // TODO: Should be fixed, we should handle this within the template and fetched properly?

        var dataGrid = /true/i.test(this.scope.attr("data_grid")),
            index = +this.scope.attr("index");

        if (dataGrid && index !== 0) {
          this.element.empty();
        }
        if (url.relevant_id && url.relevant_type) {
          var dfd = this.searchByType(url.relevant_id, url.relevant_type),
              que = new RefreshQueue();

          dfd.then(function (response) {
            var result = response.getResultsFor(url.relevant_type)[0];
            que.enqueue(result).trigger().then(function (item) {
              this.scope.filters.push({
                model_name: url.relevant_type,
                value: url.relevant_id,
                filter: result
              });
            }.bind(this));
          }.bind(this));
        }
      },
      "searchByType": function (id, type) {
        return GGRC.Models.Search.search_for_types(id, [type]);
      },
      ".add-filter-rule click": function (el, ev) {
        ev.preventDefault();
        this.scope.filters.push({
          value: "",
          filter: new can.Map(),
          model_name: this.scope.menu[0].model_singular
        });
      },
      ".ui-autocomplete-input autocomplete:select": function (el, ev, data) {
        var index = el.data("index"),
            panel = this.scope.attr("filters")[index];

        panel.attr("filter", data.item);
      },
      ".remove_filter click": function (el) {
        this.scope.filters.splice(el.data("index"), 1);
      }
    }
  });

  $("#csv_export").html(can.view(GGRC.mustache_path +
                                 "/import_export/export.mustache", {}));
})(window.can, window.can.$);
