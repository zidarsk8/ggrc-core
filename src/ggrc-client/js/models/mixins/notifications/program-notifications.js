/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from '../mixin';

export default class ProgramNotifications extends Mixin {
  get send_by_default() {
    return true;
  }

  get recipients() {
    return 'Program Managers,Program Editors,Program Readers,' +
      'Primary Contacts,Secondary Contacts';
  }
}
