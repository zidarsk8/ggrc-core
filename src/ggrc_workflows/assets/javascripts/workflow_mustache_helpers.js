/*!
    Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: dan@reciprocitylabs.com
    Maintained By: dan@reciprocitylabs.com
*/

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
