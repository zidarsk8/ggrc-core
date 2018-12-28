/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

const peopleTitlesList = [
  'Auditors', 'Principal Assignees', 'Secondary Assignees',
  'Primary Contacts', 'Secondary Contacts', 'Control Operators',
  'Control Owners',
];
const PEOPLE_VALUES_OPTIONS = Object.freeze({
  Control: [
    {value: 'Admin', title: 'Object Admins'},
    {value: 'Audit Lead', title: 'Audit Captain'},
    {value: 'Auditors', title: 'Auditors'},
    {value: 'Principal Assignees', title: 'Principal Assignees'},
    {value: 'Secondary Assignees', title: 'Secondary Assignees'},
    {value: 'Control Operators', title: 'Control Operators'},
    {value: 'Control Owners', title: 'Control Owners'},
    {value: 'Other Contacts', title: 'Other Contacts'},
    {value: 'other', title: 'Others...'},
  ],
  defaults: [
    {value: 'Admin', title: 'Object Admins'},
    {value: 'Audit Lead', title: 'Audit Captain'},
    {value: 'Auditors', title: 'Auditors'},
    {value: 'Principal Assignees', title: 'Principal Assignees'},
    {value: 'Secondary Assignees', title: 'Secondary Assignees'},
    {value: 'Primary Contacts', title: 'Primary Contacts'},
    {value: 'Secondary Contacts', title: 'Secondary Contacts'},
    {value: 'other', title: 'Others...'},
  ],
});

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
      peopleValues: {
        get: function () {
          let options = PEOPLE_VALUES_OPTIONS[
            this.attr('instance.template_object_type')
          ];
          return options ? options : PEOPLE_VALUES_OPTIONS['defaults'];
        },
      },
    },
  },
});
