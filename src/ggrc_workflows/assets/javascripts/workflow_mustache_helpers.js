/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/

;(function(can, $, Mustache) {

/*
  toggle mustache helper

  An extended "if" that sets up a "toggle_button" trigger, which can
  be applied to any button rendered within the section bounded by the
  toggle call.  toggle_buttons set the value of the toggle value to its
  boolean opposite.  Note that external forces can also set this value
  and thereby flip the toggle -- this helper is friendly to those cases.

  @helper_type section -- use outside of element tags.

  @param compute some computed value to flip between true and false

  NB: This should probably be promoted to ggrc core, as it is generally
  useful, but defer doing so until it is actually being *used* outside 
  of this extension. --BM
*/
Mustache.registerHelper("toggle", function(compute, options) {
  function toggle(trigger) {
    if (typeof trigger === "function") {
      trigger = Mustache.resolve(trigger);
    }
    if (typeof trigger !== "string") {
      trigger = "click";
    }
    return function(el) {
      $(el).bind(trigger, function() {
        compute(compute() ? false : true);
      });
    };
  }

  if (compute()) {
    return options.fn(
      options.contexts, { helpers: { toggle_button: toggle }});
  } else {
    return options.inverse(
      options.contexts, { helpers: { toggle_button: toggle }});
  }
});

/*
  sort_index_at_end mustache helper

  Given a list of items with a sort_index property, or a list of
  bindings with instances having a sort_index property, return
  a sort_index value suitable for placing a new item in the list
  at the end when sorted.

  @helper_type string -- use within attribute or outside of element

  @param list a list of objects or bindings
*/
Mustache.registerHelper("sort_index_at_end", function(list, options) {
  var max_int = Number.MAX_SAFE_INTEGER.toString(10),
      list_max = "0";
  list = Mustache.resolve(list);

  can.each(list, function(item) {
    var idx = item.sort_index || item.instance && item.instance.sort_index;
    if (typeof idx !== "undefined") {
      list_max = GGRC.Math.string_max(idx, list_max);
    }
  });

  return GGRC.Math.string_half(GGRC.Math.string_add(list_max, max_int));
});

/*
  sortable_if mustache helper

  Apply jQuery-UI sortable to the parent element if the supplied value
  is true, or false if the hash has an "inverse" key set to a truthy value

  in the other case (false for not inverse, true for inverse) the sortable
  widget attached to the element will be destroyed if it exists.

  @helper_type attributes -- use within an element tag

  @param val some computed value with a truthy or falsy value
  @param sortable_opts a JSON stringified object of options to pass to sortable
  @hashbparam inverse whether to invert the boolean check of val.
*/
Mustache.registerHelper("sortable_if", function() {
  var args = can.makeArray(arguments).slice(0, arguments.length - 1),
      options = arguments[arguments.length - 1],
      inverse = options.hash && options.hash.inverse;

  return function(el) {
    can.view.live.attributes(el, can.compute(function() {
      var val = Mustache.resolve(args[0]),
          sortable_opts = args[1];
      if (val ^ inverse) {  //value XOR inverse, one must be true, one false
        $(el).sortable(JSON.parse(sortable_opts || "{}"));
      } else if ($(el).is(".ui-sortable")) {
        $(el).sortable("destroy");
      }
    }));
  };
});

})(this.can, this.can.$, this.Mustache);
