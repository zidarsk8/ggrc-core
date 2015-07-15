/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: miha@reciprocitylabs.com
    Maintained By: miha@reciprocitylabs.com
*/

(function(can, $) {

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
        this.element.find(".csv-upload").val("");
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
          var result_count = data.reduce(function (prev, curr) {
                _.each(Object.keys(prev), function(key) {
                  prev[key] += curr[key] || 0;
                });
                return prev;
              }, {inserted: 0, updated: 0, deleted: 0, ignored: 0});

          this.scope.attr("state", "success");
          this.scope.attr("data", [result_count]);
        }.bind(this))
        .fail(function (data) {
          this.scope.attr("state", "select");
          $("body").trigger("ajax:flash", {"error": data});
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

        this.requestData = {
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
          this.scope.attr("import", _.map(data, function (element) {
            element.data = [];
            if (element.block_warnings.concat(element.row_warnings).length) {
              element.data.push({
                status: "warnings",
                messages: element.block_warnings.concat(element.row_warnings)
              });
            }
            if (element.block_errors.concat(element.row_errors).length) {
              element.data.push({
                status: "errors",
                messages: element.block_errors.concat(element.row_errors)
              });
            }
            return element;
          }));
          this.scope.attr("state", "import");
        }.bind(this))
        .fail(function (data) {
          this.scope.attr("state", "select");
          $("body").trigger("ajax:flash", {"error": data});
        }.bind(this))
        .always(function () {
          this.scope.attr("isLoading", false);
        }.bind(this));
      }
    }
  });

  $("#csv_import").html(can.view(GGRC.mustache_path + "/import_export/import.mustache", {}));
})(window.can, window.can.$);
