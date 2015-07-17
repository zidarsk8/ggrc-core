$(document).ready(function() {

  can.Component.extend({
    tag: "import",
    template: "<content/>",
    importList: [
    ],
    events: {
      "#importSelect change": function(el, ev) {
        var $value = this.element.find('option:selected').text(),
            $itemWrap = this.element.closest('.download-template').find('.import-list'),
            $item = $itemWrap.find('li'),
            index = $item.index(),
            importList = this.scope.importList;

        importList[index].attr('title', $value);

        // var $value = this.element.find('option:selected').text(),
        //     $list_value = this.element.find('.import-list'),
        //     importList = this.scope.importList;

        // $list_value.find('li').text($value);
        // importList.push({title: $value});
      }
    }
  });
  $(".import-content").html(can.view("/static/mockups/mustache/import/import.mustache",{}));

  can.Component.extend({
    tag: "import-not-pass",
    template: "<content/>",
    events: {
      ".download-template select change": function(el, ev) {
        var $value = this.element.find('option:selected').text(),
            $button_value = this.element.find('.import-button');

        $button_value.find('span').text($value);
      }
    }
  });
  $(".import-not-pass").html(can.view("/static/mockups/mustache/import/import-not-pass.mustache",{}));

  can.Component.extend({
    tag: "import-warning",
    template: "<content/>",
    events: {
      ".download-template select change": function(el, ev) {
        var $value = this.element.find('option:selected').text(),
            $button_value = this.element.find('.import-button');

        $button_value.find('span').text($value);
      }
    }
  });
  $(".import-warning").html(can.view("/static/mockups/mustache/import/import-warning.mustache",{}));

  function innerNavTrigger() {
    var $this = $(this),
        $allList = $this.closest(".nav").children("li"),
        $list = $this.closest("li"),
        aId = $this.attr("href"),
        $element = $("div"+aId);

    $(".import-main").hide();
    $(".import-main"+aId).show();
  }

  function chooseCSV() {
    $("#chooseFile").fadeOut(500);
    $("#analysingFile").delay(500).fadeIn(500);
    $(".import-main-wrap-analyze").delay(1500).fadeIn(500);
    $("#analysingFile").delay(2000).fadeOut(500);
    $("#importFile").delay(3500).fadeIn(500);
  }

  function chooseCSV2() {
    $("#chooseFile2").fadeOut(500);
    $("#analysingFile2").delay(500).fadeIn(500);
    $(".import-main-wrap-analyze").delay(1500).fadeIn(500);
    $("#analysingFile2").delay(1500).fadeOut(500);
    $("#chooseFile2").delay(2500).fadeIn(500);
  }

  function chooseCSV3() {
    $("#chooseFile3").fadeOut(500);
    $("#analysingFile3").delay(500).fadeIn(500);
    $(".import-main-wrap-analyze").delay(1500).fadeIn(500);
    $("#analysingFile3").delay(2000).fadeOut(500);
    $("#importFile3").delay(3500).fadeIn(500);
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
    $(".import-main-wrap-analyze").delay(4000).fadeOut(500);
    $(".import-final").delay(4500).fadeIn(500);
  }

  function importing2() {
    $("#importFile3").fadeOut(500);
    $("#importingFile3").delay(500).fadeIn(500);
    $(".import-progress").delay(500).fadeIn(500);
    $(".import-analyze h4").delay(1500).fadeOut(500);
    $("#importingFile3").delay(2000).fadeOut(500);
    $("#importedFile3").delay(3500).fadeIn(500);
    $(".import-progress").delay(2000).fadeOut(500);
    $(".import-progress-final").delay(3500).fadeIn(500);
    $(".import-main-wrap-analyze").delay(4000).fadeOut(500);
    $(".import-final").delay(4500).fadeIn(500);
  }

  $(".top-inner-nav a").on("click", innerNavTrigger);
  $("#chooseFile").on("click", chooseCSV);
  $("#importFile").on("click", importing);

  $("#chooseFile2").on("click", chooseCSV2);
  $("#chooseFile3").on("click", chooseCSV3);
  $("#importFile3").on("click", importing2);

});
