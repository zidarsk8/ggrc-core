/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';

export default Mixin('scope-object-notifications', {
  send_by_default: true,
  recipients: 'Admin,Assignee,Verifier,Compliance Contacts,Product Managers,' +
  'Technical Leads,Technical / Program Managers,Legal Counsels,System Owners',
});
