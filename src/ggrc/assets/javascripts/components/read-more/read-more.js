/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/read-more/read-more.mustache');
  var tag = 'read-more';
  var readMore = 'Read More';
  var readLess = 'Read Less';
  var classPrefix = 'ellipsis-truncation-';
  /**
   * Assessment specific read more view component
   */
  GGRC.Components('readMore', {
    tag: tag,
    template: tpl,
    viewModel: {
      define: {
        text: {
          type: 'string',
          set: function (newValue) {
            return GGRC.Utils.getPlainText(newValue);
          }
        },
        maxLinesNumber: {
          type: 'number',
          value: 5
        },
        cssClass: {
          type: 'string',
          value: '',
          get: function () {
            return this.attr('expanded') ? '' :
              classPrefix + this.attr('maxLinesNumber');
          }
        }
      },
      expanded: false,
      overflowing: false,
      lineHeight: null,
      btnText: function () {
        return this.attr('expanded') ? readLess : readMore;
      },
      toggle: function (viewModel, el, ev) {
        ev.stopPropagation();
        this.attr('expanded', !this.attr('expanded'));
      },
      isOverflowing: function (element) {
        var result;
        var clientHeight = element.clientHeight;
        var scrollHeight = element.scrollHeight;

        if (!this.attr('expanded')) {
          result = scrollHeight > clientHeight;
        } else {
          result = clientHeight >=
            (this.attr('lineHeight') * this.attr('maxLinesNumber'));
        }
        this.attr('overflowing', result);
      }
    },
    events: {
      inserted: function () {
        var $element = $(this.element).find('.read-more__body');

        this.viewModel.attr('lineHeight',
          parseInt($element.css('line-height'), 10));
      },
      '{element} mouseover': function (ev) {
        var element = $(this.element).find('.read-more__body')[0];

        if (element) {
          this.viewModel.isOverflowing(element);
        }
      }
    }
  });
})(window.can, window.GGRC);
