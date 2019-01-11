/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (root, GGRC, $, can) {
  let doc = root.document;
  let body = doc.body;
  let $win = $(root);
  let $doc = $(doc);
  let $body = $(body);

  $.migrateMute = true; // turn off console warnings for jQuery-migrate

  root.calculate_spinner_z_index = function () {
    let zindex = 0;
    $(this).parents().each(function () {
      let z = parseInt($(this).css('z-index'), 10);
      if (z) {
        zindex = z;
        return false;
      }
    });
    return zindex + 10;
  };

  $doc.ready(function () {
    // monitor target, where flash messages are added
    let AUTOHIDE_TIMEOUT = 10000;
    let timeoutId;
    let target = $('section.content div.flash')[0];
    let observer = new MutationObserver(function (mutations) {
      mutations.forEach(function (mutation) {
        // check for new nodes
        if (mutation.addedNodes && mutation.addedNodes.length > 0) {
          // remove the success message from non-expandable
          // flash success messages after timeout
          clearTimeout(timeoutId);

          timeoutId = setTimeout(function () {
            $('.flash .alert-autohide').remove();
          }, AUTOHIDE_TIMEOUT);
        }
      });
    });

    let config = {
      attributes: true,
      childList: true,
      characterData: true,
    };

    if (target) {
      observer.observe(target, config);
    }
  });

  $win.load(function () {
    $body.on('click', 'ul.tree-structure .item-main .openclose', function (ev) {
      ev.stopPropagation();
      $(this).openclose();
    });
  });

  // Make sure GGRC.config is defined (needed to run Karma tests)
  GGRC.config = GGRC.config || {};
})(window, GGRC, jQuery, can);
