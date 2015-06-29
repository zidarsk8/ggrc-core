/*!
  Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
  Created By: ivan@reciprocitylabs.com
  Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $) {
  can.Component.extend({
    tag: "csv-export",
    template: "<content></content>",
    scope: {
      url: "/_service/export_csv",
      editFilename: false,
      filename: function () {
        return "Export Objects";
      }
    },
    events: {
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
          this._panels.push({
            type: "Programs",
            index: 0
          });
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
          data.type = "Programs";
        }

        this.scope.attr("_index", index);
        data.index = index;
        return this.scope.attr("_panels").push(data);
      },
      ".remove_filter_group click": function (el, ev) {
        ev.preventDefault();
        var index = this.getIndex(el);
        this.scope.attr("_panels").splice(index, 1);
      },
      "#addAnotherObjectType click": function (el, ev) {
        ev.preventDefault();
        this.addPanel();
      },
      "export-panel .option-type-selector change": function (el, ev) {
        var $el = $(ev.currentTarget),
            val = $el.val(),
            index = this.getIndex($el);
      }
    }
  });

  can.Component.extend({
    tag: "export-panel",
    template: "<content></content>",
    scope: {
      index: "@"
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
      panels: [],
      menu: can.map(["Program", "Regulation", "Policy", "Standard", "Contract",
                    "Clause", "Section", "Objective", "Control", "Person", 
                    "System", "Process", "DataAsset", "Product", "Project",
                    "Facility", "Market"], 
                    function (key) {
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

  $("#csv_export").html(can.view(GGRC.mustache_path + 
                                 "/import_export/export.mustache", {}));
})(window.can, window.can.$);
