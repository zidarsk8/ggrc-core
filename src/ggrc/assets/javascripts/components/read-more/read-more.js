/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/read-more/read-more.mustache');
  var tag = 'read-more';
  var defaultTextLength = 200;
  var readMore = 'Read More';
  var readLess = 'Read Less';
  var overflowPostfix = '...';
  /**
   * Assessment specific read more view component
   */
  GGRC.Components('readMore', {
    tag: tag,
    template: tpl,
    scope: {
      maxTextLength: '@',
      text: null,
      expanded: false,
      resultedText: null,
      overflowing: false,
      btnText: function () {
        return this.attr('expanded') ? readLess : readMore;
      },
      toggle: function (scope, el, ev) {
        ev.stopPropagation();
        this.attr('expanded', !this.attr('expanded'));
      },
      /**
       * Get Limited text string
       * @param {String} text - is original text
       * @param {Number} limit - is maximum allowed text length
       * @return {string} - returns resulted text part with "..." ending
         */
      getSlicedText: function (text, limit) {
        // As we add extra postfix at the end - remove it's length from the limit
        limit -= overflowPostfix.length;
        return text.slice(0, limit) + overflowPostfix;
      },
      setValues: function (originalText) {
        var limit = Number(this.attr('maxTextLength')) || defaultTextLength;
        var trimmedText = GGRC.Utils.getPlainText(originalText);
        var isOverflowing = trimmedText.length >= limit;
        this.attr('maxTextLength', limit);
        this.attr('overflowing', isOverflowing);
        this.attr('resultedText', isOverflowing ?
          this.getSlicedText(trimmedText, limit) :
          originalText);
      }
    },
    events: {
      init: function () {
        this.scope.setValues(this.scope.attr('text'));
      },
      '{scope} text': function (scope, ev, val) {
        this.scope.setValues(val);
      }
    }
  });
})(window.can, window.GGRC);
