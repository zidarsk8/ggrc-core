/*!
    Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: anze@reciprocitylabs.com
    Maintained By: anze@reciprocitylabs.com
*/


(function (can, $) {

  // Only load this file when the URL is mockups/sample:
  if (window.location.pathname !== "/mockups/request") {
    return;
  }

  // Setup the object page:
  var mockup = new CMS.Controllers.MockupHelper($('body'), {
    // Object:
    object: {
      icon: "grciconlarge-audit",
      title: "Request",
    },
    // Views:
    views: [{
        // Example on how to use an existing template:
        title: "Info",
        icon: "grcicon-info",
        template: "/request/info.mustache"
      }
    ],
  });
})(this.can, this.can.$);
