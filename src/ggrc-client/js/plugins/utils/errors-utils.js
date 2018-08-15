/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {
  notifier,
  notifierXHR,
  messages,
} from './notifiers-utils';

function isConnectionLost() {
  return !navigator.onLine;
}

function handleAjaxError(jqxhr, errorThrown = '') {
  let isExpectedError = jqxhr.getResponseHeader('X-Expected-Error');

  if (!isExpectedError) {
    let response = jqxhr.responseJSON;

    if (!response) {
      try {
        response = JSON.parse(jqxhr.responseText);
      } catch (e) {
        console // eslint-disable-line no-console
          .warn('Response not in JSON format');
      }
    }

    let message = jqxhr.getResponseHeader('X-Flash-Error') ||
      messages[jqxhr.status] ||
      (response && response.message) ||
      errorThrown.message || errorThrown;

    if (message) {
      notifier('error', message);
    } else {
      notifierXHR('error')(jqxhr);
    }
  }
}

export {
  isConnectionLost,
  handleAjaxError,
};
