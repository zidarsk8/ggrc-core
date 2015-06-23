/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: miha@reciprocitylabs.com
    Maintained By: miha@reciprocitylabs.com
*/

(function(can, $) {

  can.Component.extend({
    tag: "csv-template",
    template: "<content></content>",
    scope: {
      url: "/_service/export_csv",
      selected: []
    },
    events: {
      "#importSelect change": function (el, ev) {
        var $items = el.find(":selected"),
            selected = this.scope.attr("selected");

        function isSelected(val) {
          return ;
        }
        $items.each(function () {
          var $item = $(this);
          if (_.findWhere(selected, {value: $item.val()})) {
            return;
          }
          return selected.push({
            name: $item.attr("label"),
            value: $item.val()
          });
        });
      },
      ".import-button click": function (el, ev) {
        ev.preventDefault();
        var data = _.reduce(this.scope.attr("selected"), function (memo, item) {
                memo[item.value] = [];
                return memo;
              }, {});
        // data = {
        //   "Section": [1, 2, 3]
        // }
        $.ajax({
          type: "POST",
          dataType: "json",
          headers: {
            "Content-Type": "application/json",
            "X-test-only": "true",
            "X-requested-by": "gGRC"
          },
          url: this.scope.attr("url"),
          data: data
        });
      },
      ".import-list a click": function (el, ev) {
        ev.preventDefault();

        var index = el.data("index"),
            item = this.scope.attr("selected").splice(index, 1)[0];

        this.element.find("#importSelect option:selected").each(function () {
          var $item = $(this);
          if ($item.val() === item.value) {
            $item.prop("selected", false);
          }
        });
      }
    }
  });

  can.Component.extend({
    tag: "csv-import",
    template: "<content></content>",
    requestData: null,
    scope: {
      importUrl: "/_service/import_csv",
      import: null,
      filename: "",
      isLoading: false,
      state: "select",
      states: function () {
        var state = this.attr("state") || "select",
            states = {
              select: {class: "btn-success", text: "Choose CSV file to import"},
              analyse: {class: "btn-draft", text: "Analysing", isDisabled: true},
              import: {class: "btn-primary", text: "Import data"},
              importing: {class: "btn-draft", text: "Importing", isDisabled: true},
              success: {class: "btn-success", text: "<i class=\"grcicon-check-white\"></i> Import successful"}
            };

        return _.extend(states[state], {state: state});
      }
    },
    events: {
      ".state-reset click": function (el, ev) {
        ev.preventDefault();
        this.scope.attr({
          state: "select",
          filename: "",
          import: null
        });
      },
      ".state-select click": function (el, ev) {
        ev.preventDefault();
        this.element.find(".csv-upload").trigger("click");
      },
      ".state-import click": function (el, ev) {
        ev.preventDefault();
        this.scope.attr("state", "importing");
        this.requestData.headers["X-test-only"] = "false";

        $.ajax(this.requestData)
        .done(function (data) {
          var result_count = data.reduce(function(prev, curr){
            _.each(Object.keys(prev), function(key){
              prev[key] += curr[key] || 0;
            });
            return prev
          }, {inserted: 0, updated: 0, deleted: 0, ignored: 0})

          this.scope.attr("state", "success");
          this.scope.attr("data", [result_count]);
        }.bind(this))
        .fail(function (data) {
          this.scope.attr("state", "select");
          // TODO: write error
        }.bind(this))
        .always(function () {
          this.scope.attr("isLoading", false);
        }.bind(this));
      },
      ".csv-upload change": function (el, ev) {
        var file = el[0].files[0],
            formData = new FormData();

        this.scope.attr("state", "analysing");
        this.scope.attr("isLoading", true);
        this.scope.attr("filename", file.name);
        formData.append("file", file);

        this.requestData =  {
          type: "POST",
          url: this.scope.attr("importUrl"),
          data: formData,
          cache: false,
          contentType: false,
          processData: false,
          headers: {
            "X-test-only": "true",
            "X-requested-by": "gGRC"
          }
        };

        $.ajax(this.requestData)
        .done(function (data) {
          this.scope.attr("import", _.map(data, function (element){
            element.data = [
              { status: "warnings",
                messages: element.block_warnings.concat(element.row_warnings)
              },
              { status: "errors",
                messages: element.block_errors.concat(element.row_errors)
              },
            ];
            return element;
          }));
          this.scope.attr("state", "import");
        }.bind(this))
        .fail(function (data) {
          this.scope.attr("state", "select");
          // TODO: write error
        }.bind(this))
        .always(function () {
          this.scope.attr("isLoading", false);
        }.bind(this));
      }
    }
  });

  $("#csv_import").html(can.view(GGRC.mustache_path + "/import_export/import.mustache", {}));
})(window.can, window.can.$);
