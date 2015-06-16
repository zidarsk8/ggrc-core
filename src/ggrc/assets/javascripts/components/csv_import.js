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
      import_state: "@",
      button_states: {
        select_file: {class: "btn-success", text: "Choose CSV file to import"},
        analysing_file: {class: "btn-draft", text: "Analysing"},
        importing_file: {class: "btn-draft", text: "Importing"},
      }
    },
    template: can.view(GGRC.mustache_path + "/import_export/import.mustache"),
    events: {
    },
    helpers: {
      with_button_state: function(state, options){
        state = Mustache.resolve(state)
        return options.fn(options.contexts.add(
            options.context.button_states[state]));
      }
    }
  });

  var template = can.view.mustache($("#csv_import").html());
  $("#csv_import").html( template() );
});

})(window.can, window.can.$);
