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

  function chooseCSV() {
    $("#chooseFile").fadeOut(500);
    $("#analysingFile").delay(500).fadeIn(500);
    $(".import-analyze").delay(1500).fadeIn(500);
    $("#analysingFile").delay(2000).fadeOut(500);
    $("#importFile").delay(3500).fadeIn(500);
  }

  function importing() {
    $("#importFile").fadeOut(500);
    $("#importingFile").delay(500).fadeIn(500);
    $(".import-progress").delay(500).fadeIn(500);
    $(".import-analyze h4").delay(1500).fadeOut(500);
    $("#importingFile").delay(2000).fadeOut(500);
    $("#importedFile").delay(3500).fadeIn(500);
    $(".import-progress").delay(2000).fadeOut(500);
    $(".import-progress-final").delay(3500).fadeIn(500);
    $(".import-analyze").delay(4000).fadeOut(500);
    $(".import-final").delay(4500).fadeIn(500);
  }

  $("#chooseFile").on("click", chooseCSV);
  $("#importFile").on("click", importing);

});
