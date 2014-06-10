/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/

;(function(can, $, Mustache) {

Mustache.registerHelper("toggle", function(compute, options) {
  function toggle(trigger) {
    if(typeof trigger === "function") {
      trigger = Mustache.resolve(trigger);
    }
    if(typeof trigger !== "string") {
      trigger = "click";
    }
    return function(el) {
      $(el).bind(trigger, function() {
        compute(compute() ? false : true);
      });
    };
  }

  if(compute()) {
    return options.fn(options.contexts, { helpers : { toggle_button : toggle }});
  } else {
    return options.inverse(options.contexts, { helpers : { toggle_button : toggle }});
  }
});

Mustache.registerHelper("sort_index_at_end", function(list, options) {
  var max_int = Number.MAX_SAFE_INTEGER.toString(10),
    list_max = "0";
  list = Mustache.resolve(list);

  can.each(list, function(item) {
    var idx = item.sort_index || item.instance && item.instance.sort_index;
    if(typeof idx !== "undefined") {
      list_max = GGRC.Math.string_max(idx, list_max);
    }
  });

  return GGRC.Math.string_half(GGRC.Math.string_add(list_max, max_int));
});

})(this.can, this.can.$, this.Mustache);
