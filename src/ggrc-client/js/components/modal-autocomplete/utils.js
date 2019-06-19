/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Stub from '../../models/stub';
import {initAuditTitle} from '../../plugins/utils/models-utils';
import canMap from 'can-map';

export const onAutocompleteKeyup = (instance, el, ev) => {
  // * in some cases we want to disable automapping the selected item to the
  // * modal's underlying object (e.g. we don't want to map the picked Persons
  // * to an AssessmentTemplates object)
  // ** does nothing after press tab to not lose default value in input
  if (el.data('no-automap') || ev.keyCode === 9) {
    return;
  }

  // Set the transient field for validation
  const name = el.attr('name').split('.');
  const value = el.val();

  name.pop(); // set the owner to null, not the email

  if (!instance._transient) {
    instance.attr('_transient', new canMap({}));
  }

  _.reduce(name.slice(0, -1), function (current, next) {
    current = current + '.' + next;
    if (!instance.attr(current)) {
      instance.attr(current, new canMap({}));
    }
    return current;
  }, '_transient');

  if (name.length) {
    instance.attr(['_transient'].concat(name).join('.'), value);
  }
};

export const onAutocompleteSelect = (
  instance, isNewInstance
) => (el, ui) => {
  let path;
  let index;
  let cb;
  $('#extended-info').trigger('mouseleave'); // Make sure the extra info tooltip closes

  path = el.attr('name').split('.');
  index = 0;
  path.pop(); // remove the prop
  cb = el.data('lookup-cb');

  if (cb) {
    cb = cb.split(' ');
    instance[cb[0]](...cb.slice(1).concat([ui.item]));
    setTimeout(function () {
      el.val(ui.item.name || ui.item.email || ui.item.title, ui.item);
    }, 0);
    return;
  }

  if (/^\d+$/.test(path[path.length - 1])) {
    index = parseInt(path.pop(), 10);
    path = path.join('.');
    if (!instance.attr(path)) {
      instance.attr(path, []);
    }
    instance.attr(path).splice(index, 1, new Stub(ui.item));
  } else {
    path = path.join('.');
    setTimeout(function () {
      el.val(ui.item.name || ui.item.email || ui.item.title, ui.item);
    }, 0);

    instance.attr(path, null).attr(path, ui.item);
    initAuditTitle(instance, isNewInstance);
    if (!instance._transient) {
      instance.attr('_transient', canMap());
    }
    instance.attr('_transient.' + path, ui.item);
  }
};
