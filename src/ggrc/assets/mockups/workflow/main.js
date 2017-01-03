/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/


(function (can, $) {

  // Only load this file when the URL is mockups/sample:
  if (window.location.pathname !== "/mockups/workflow") {
    return;
  }

  // Setup the object page:
  var mockup = new CMS.Controllers.MockupHelper($("body"), {
    // Object:
    object: {
      icon: "workflow",
      title: "Workflow",
    },
    // Views:
    views: _.values(GGRC.Bootstrap.Mockups.Workflow)
  });
})(this.can, this.can.$);
