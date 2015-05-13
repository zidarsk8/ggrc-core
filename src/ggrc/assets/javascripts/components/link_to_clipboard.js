/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $, Clipboard) {
  "use strict";

  can.Component.extend({
    tag: "clipboard-link",
    scope: {
      text: "@",
      title: "@",
      notify: "@",
      isActive: false,
      timeout: "@",
      notifyText: "Link has been copied to your clipboard."
    },
    template: ["<a data-clipboard-text=\"{{text}}\" {{#isActive}}class=\"active\"{{/isActive}} href=\"#\">",
               "<i class=\"icon-share\"></i> {{title}}",
               "</a>"].join(""),
    events: {
      "a click": function (el, evnt) {
        evnt.preventDefault();
      },
      "inserted": function (el, evnt) {
        var timeout = this.scope.attr("timeout") || 10000;
        this._clip = new Clipboard(el.find("a"));

        this._clip.on("aftercopy", function () {
          if (this.scope.attr("notify")) {
            $("body").trigger("ajax:flash", {"success": this.scope.attr("notifyText")});
          }
          this.scope.attr("isActive", true);
          setTimeout(function () {
            this.scope.attr("isActive", false);
          }.bind(this), timeout);
        }.bind(this));
      }
    }
  });

})(window.can, window.can.$, window.ZeroClipboard);
