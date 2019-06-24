/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
import './confirm-edit-action';
import template from './assessment-inline-item.stache';

export default CanComponent.extend({
  tag: 'assessment-inline-item',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    instance: {},
    propName: '',
    value: '',
    type: '',
    dropdownOptions: [],
    dropdownOptionsGroups: {},
    dropdownClass: '',
    isGroupedDropdown: false,
    dropdownNoValue: false,
    withReadMore: false,
    isEditIconDenied: false,
    onStateChangeDfd: $.Deferred().resolve(),
    mandatory: false,
    isConfirmationNeeded: true,
  }),
});
