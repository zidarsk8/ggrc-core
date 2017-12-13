/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import template from './read-more.mustache';

const readMore = 'Read More';
const readLess = 'Read Less';
const classPrefix = 'ellipsis-truncation-';
const viewModel = {
  define: {
    text: {
      type: 'string',
      value: '',
    },
    maxLinesNumber: {
      type: 'number',
      value: 5,
    },
    cssClass: {
      type: 'string',
      value: '',
      get() {
        return this.attr('expanded') ? '' :
          classPrefix + this.attr('maxLinesNumber');
      },
    },
  },
  expanded: false,
  overflowing: false,
  lineHeight: null,
  btnText() {
    return this.attr('expanded') ? readLess : readMore;
  },
  toggle(ev) {
    ev.stopPropagation();
    this.attr('expanded', !this.attr('expanded'));
  },
  checkOverflowing(el) {
    const $element = $(el).find('.read-more__body');
    const element = $element[0];

    this.attr('lineHeight',
      parseInt($element.css('line-height'), 10));

    if (element) {
      this.isOverflowing(element);
    }
  },
  isOverflowing(element) {
    let result;
    const clientHeight = element.clientHeight;
    const scrollHeight = element.scrollHeight;

    if (!this.attr('expanded')) {
      result = scrollHeight > clientHeight;
    } else {
      result = clientHeight >=
        (this.attr('lineHeight') * this.attr('maxLinesNumber'));
    }
    this.attr('overflowing', result);
  },
};

export default can.Component.extend({
  tag: 'read-more',
  template,
  viewModel,
  events: {
    '{element} mouseover'() {
      this.viewModel.checkOverflowing(this.element);
    },
  },
});
