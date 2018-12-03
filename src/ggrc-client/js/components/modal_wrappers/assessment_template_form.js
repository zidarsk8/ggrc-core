/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

const peopleTitlesList = [
  'Auditors', 'Principal Assignees', 'Secondary Assignees',
  'Primary Contacts', 'Secondary Contacts',
];

export default can.Component.extend({
  tag: 'wrapper-assessment-template',
  viewModel: {
    instance: {},
    define: {
      showCaptainAlert: {
        type: 'boolean',
        value: false,
        get() {
          return peopleTitlesList
            .includes(this.attr('instance.default_people.assignees'));
        },
      },
    },
  },
});
