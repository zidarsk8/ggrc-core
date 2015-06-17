/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: miha@reciprocitylabs.com
    Maintained By: miha@reciprocitylabs.com
*/

(function(can, $) {

$(function() {

  can.Component.extend({
    tag: "csv-import",
    scope: {
      csv_import_url: "/_service/import_csv",
      import_state: "@",
      import_info: [],
      import_errors: [],
      import_warnings: [],
      button_states: {
        select_file: {class: "btn-success", text: "Choose CSV file to import"},
        analysing_file: {class: "btn-draft", text: "Analysing"},
        import_file: {class: "btn-primary", text: "Import data"},
        importing_file: {class: "btn-draft", text: "Importing"},
      },
      upload_file: function(file){
        var form_data = new FormData();

        this.attr("import_state", "analysing_file");
        form_data.append('file', file);

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
        }).done(function(data){
          console.log(data);
          _.forIn(data, function(value, key){
            this.attr("import_"+key, value);
          }.bind(this));
          this.attr("import_state", "import_file");
        }.bind(this)).fail(function(e){
          this.attr("import_state", "select_file");
          // TODO: write error
        }.bind(this));
      }
    },
    template: can.view(GGRC.mustache_path + "/import_export/import.mustache"),
    events: {
      "#import_btn click": function (el, ev) {
        switch (this.scope.import_state) {
          case "select_file":
            $("[data-file-upload]").trigger("click");
            break;
          case "import_file":
            break;
        }
        ev.preventDefault();
      },
      "[data-file-upload] change": function(el, ev){
        var file = el[0].files[0];
        this.scope.upload_file(file);
      }
    },
    helpers: {
      with_button_state: function(state, options){
        state = Mustache.resolve(state)
        return options.fn(options.contexts.add(
            options.context.button_states[state]));
      }
    }
  });
  
  var $import = $("#csv_import");
  if ($import){
    $import.html(can.view.mustache($import.html()));
  }
});

})(window.can, window.can.$);
