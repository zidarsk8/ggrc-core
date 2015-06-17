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
    scope: {
      csv_import_url: "/_service/import_csv",
      // import_state: "@",
      import_info: [],
      import_errors: [],
      import_warnings: [],
      state: "select",
      states: function () {
        var states = {
          select: {class: "btn-success", text: "Choose CSV file to import"},
          analyse: {class: "btn-draft", text: "Analysing"},
          import: {class: "btn-primary", text: "Import data"},
          importing: {class: "btn-draft", text: "Importing"}
        };
        console.log("States", this, arguments);
        return states[this.attr("state")] || states["select"];
      },
      upload_file: function (file) {
        var form_data = new FormData();

        this.attr("import_state", "analysing_file");
        form_data.append("file", file);

        $.ajax({
          type: "POST",
          url: this.csv_import_url,
          data: form_data,
          cache: false,
          contentType: false,
          processData: false,
          headers: {
            "X-test-only": "true",
            "X-requested-by": "gGRC"
          }
        }).done(function (data) {
          console.log(data);
          _.forIn(data, function (value, key) {
            this.attr("import_" + key, value);
          }.bind(this));
          this.attr("import_state", "import_file");
        }.bind(this)).fail(function (e) {
          this.attr("import_state", "select_file");
          // TODO: write error
        }.bind(this));
      }
    },
    events: {
      "#import_btn click": function (el, ev) {
        ev.preventDefault();
        var states = "select analyse import importing".split(" ");

        // switch (this.scope.import_state) {
        //   case "select_file":
        //     $("[data-file-upload]").trigger("click");
        //     break;
        //   case "import_file":
        //     break;
        // }
      },
      "[data-file-upload] change": function(el, ev) {
        var file = el[0].files[0];
        this.scope.upload_file(file);
      }
    },
    helpers: {
      with_button_state: function (state, options) {
        state = Mustache.resolve(state);
        return options.fn(options.contexts.add(
            options.context.button_states[state]));
      }
    }
  });

  $("#csv_import").html(can.view(GGRC.mustache_path + "/import_export/import.mustache", {}));
})(window.can, window.can.$);
