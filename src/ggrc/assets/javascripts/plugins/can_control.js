/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: ivan@reciprocitylabs.com
    Maintained By: ivan@reciprocitylabs.com
*/

(function(can) {
  can.extend(can.Control.prototype, {
    // Returns a function which will be halted unless `this.element` exists
    //   - useful for callbacks which depend on the controller's presence in
    //     the DOM
    _ifNotRemoved: function(fn) {
      var that = this;
      return function() {
        if (!that.element) {
          return;
        }
        return fn.apply(this, arguments);
      };
    },

    //make buttons non-clickable when saving
    bindXHRToButton : function(xhr, el, newtext, disable) {
      // binding of an ajax to a click is something we do manually
      var $el = $(el)
      , oldtext = $el.text();

      if(newtext) {
        $el[0].innerHTML = newtext;
      }
      $el.addClass("disabled pending-ajax");
      if (disable !== false) {
        $el.attr("disabled", true);
      }
      xhr.always(function() {
        // If .text(str) is used instead of innerHTML, the click event may not fire depending on timing
        if ($el.length) {
          $el.removeAttr("disabled").removeClass("disabled pending-ajax")[0].innerHTML = oldtext;
        }
      });
    }
  });
})(this.can);
