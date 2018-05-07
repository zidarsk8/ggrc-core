/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import template from './release-notes.md';

const events = {
  ['a click'](el, event) {
    const id = el.attr('href');

    const linkedHeader = this.element.find(id)[0];

    if (linkedHeader) {
      event.preventDefault();

      linkedHeader.scrollIntoView({
        behavior: 'smooth',
        block: 'start',
      });
    }
  },
};

export default can.Component.extend({
  tag: 'release-notes-list',
  template,
  events,
});
