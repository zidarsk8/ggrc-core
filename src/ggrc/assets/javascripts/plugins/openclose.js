/*!
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function ($) {
  function openclose(command) {
    var $that = $(this);
    var useSlide = $that.length < 100;

    $that.each(function () {
      var $this = $(this);
      var $main = $this.closest('.item-main');
      var $li = $main.closest('li');
      var $content = $li.children('.item-content');
      var $peopleInfo = $li.children('people-list-info');
      var $icon = $main.find('.openclose');
      var $parentTree = $this.closest('ul.new-tree');
      var cmd = command;

      if (typeof cmd !== 'string' || cmd === 'toggle') {
        cmd = $icon.hasClass('active') ? 'close' : 'open';
      }

      if (cmd === 'close') {
        if (useSlide) {
          $content.slideUp('fast');
        } else {
          $content.css('display', 'none');
        }
        $icon.removeClass('active');
        $li.removeClass('item-open');
        // Only remove tree open if there are no open siblings
        if (!$li.siblings('.item-open').length) {
          $parentTree.removeClass('tree-open');
        }
        $content.removeClass('content-open');
        can.trigger($peopleInfo, 'click', true);
      } else if (cmd === 'open') {
        if (useSlide) {
          $content.slideDown('fast');
        } else {
          $content.css('display', 'block');
        }
        $icon.addClass('active');
        $li.addClass('item-open');
        $parentTree.addClass('tree-open');
        $content.addClass('content-open');
        can.trigger($peopleInfo, 'click', false);
      }
    });

    return this;
  }
  $.fn.openclose = openclose;
})(jQuery);
