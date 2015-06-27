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

  $("#csv_export").html(can.view(GGRC.mustache_path + "/import_export/export.mustache", {}));
})(window.can, window.can.$);
