/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from '../mixin';

export default class CycleTaskNotifications extends Mixin {
  get send_by_default() { // eslint-disable-line camelcase
    return true;
  }

  get recipients() {
    return 'Task Assignees,Task Secondary Assignees';
  }
}
