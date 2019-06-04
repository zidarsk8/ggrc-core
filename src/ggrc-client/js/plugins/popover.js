/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

const body = $('body');

$.fn.modal_showhide = showhide('.modal', '.hidden-fields-area');
$.fn.widget_showhide = showhide('.info', '.hidden-fields-area');
$.fn.issue_tracker_modal_showhide = showhide('.modal',
  '.hidden-issue-tracker-fields-area');

body.on('click', '.expand-link a', $.fn.modal_showhide);
body.on('click', '.info-expand a', $.fn.widget_showhide);
body.on('click',
  '.expand-issue-tracker-link a', $.fn.issue_tracker_modal_showhide);

function showhide(upsel, downsel) {
  return function (command) {
    $(this).each(function () {
      let $this = $(this);
      let $content = $this.closest(upsel).find(downsel);
      let cmd = command;

      if (typeof cmd !== 'string' || cmd === 'toggle') {
        cmd = $this.hasClass('active') ? 'hide' : 'show';
      }
      if (cmd === 'hide') {
        $content.slideUp();
        $this.removeClass('active');
      } else if (cmd === 'show') {
        $content.slideDown();
        $this.addClass('active');
      }
    });

    return this;
  };
}
