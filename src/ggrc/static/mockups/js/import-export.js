$(document).ready(function() {

  can.Component.extend({
    tag: "import",
    scope: {
      report_gen: false,
    },
    template: "<content/>",
    helpers: {
    },
    events: {
      ".download-template select change": function(el, ev) {
        var $value = this.element.find('option:selected').text(),
            $button_value = this.element.find('.import-button');

        $button_value.find('span').text($value);
      }
    }
  });

  $(".import-content").html(can.view("/static/mockups/mustache/import-export.mustache",{}));

});
