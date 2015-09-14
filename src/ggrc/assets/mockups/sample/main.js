/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/


(function (can, $) {

  // Only load this file when the URL is mockups/sample:
  if (window.location.pathname !== "/mockups/sample") {
    return;
  }

  // Setup the object page:
  var mockup = new CMS.Controllers.MockupHelper($("body"), {
    // Object:
    object: {
      icon: "grciconlarge-program",
      title: "Program",
    },
    // Views:
    views: [{
        // Example on how to use an existing template:
        title: "Info",
        icon: "grcicon-info",
        template: "/base_objects/info.mustache",
      }, {
        // An example for a custom template:
        title: "Counter",
        icon: "grcicon-objective-color",
        template: "/sample/sample.mustache",
        // Scope parameters for the template:
        scope: new can.Map({
          count: 0,
        }),
        events: {
          // Events that can trigger updates on the template:
          "button click": function () {
            this.scope.attr("count", this.scope.count + 1);
          }
        }
      }
    ],
  });
})(this.can, this.can.$);
