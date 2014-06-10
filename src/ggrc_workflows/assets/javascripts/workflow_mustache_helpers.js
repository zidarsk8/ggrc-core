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

Mustache.registerHelper("sortable_if", function() {
  var args = can.makeArray(arguments).slice(0, arguments.length - 1),
    options = arguments[arguments.length - 1];
  var val, inverse = false;
  if(args[0] === "not") {
    args.shift();
    inverse = true;
  }

  return function(el) {
    can.view.live.attributes(el, can.compute(function() {
      var val = Mustache.resolve(args[0]);
      if(val ^ inverse) {  //value XOR inverse, one must be true, one false
        $(el).sortable(JSON.parse(args[1] || "{}"));
      } else if($(el).is(".ui-sortable")) {
        $(el).sortable("destroy");
      }
    }));
  };
});

})(this.can, this.can.$, this.Mustache);
