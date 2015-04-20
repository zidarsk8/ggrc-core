/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function(can, $, Clipboard) {
  "use strict";

  can.Component.extend({
    tag: "clipboard_link",
    scope: {
      clipboard_text: null,
      isActive: false,
      timeout: 10000
    },
    template: ["<a data-clipboard-text=\"{{clipboard_text}}\" {{#isActive}}class=\"active\"{{/isActive}} href=\"#\">",
               "<i class=\"icon-share\"></i> Get permalink",
               "</a>"].join(""),
    events: {
      "a click": function (el, evnt) {
        evnt.preventDefault();
      },
      "inserted": function (el, evnt) {
        this._clip = new Clipboard(el.find("a"));
        this.scope.attr("clipboard_text", window.location.href);

        this._clip.on("aftercopy", function () {
          this.scope.attr("isActive", true);
          setTimeout(function () {
            this.scope.attr("isActive", false);
          }.bind(this), this.scope.attr("timeout"));
        }.bind(this));
      }
    }
  });

})(window.can, window.can.$, window.ZeroClipboard);
