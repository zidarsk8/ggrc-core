/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import './info-pane/confirm-edit-action';
import template from './custom-attributes.stache';

export default CanComponent.extend({
  tag: 'assessment-custom-attributes',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    items: [],
    editMode: false,
    modifiedFields: {},
    isEditDenied: false,
    updateGlobalAttribute: function (event, field) {
      this.attr('modifiedFields').attr(field.customAttributeId, event.value);
      this.dispatch({
        type: 'onUpdateAttributes',
        globalAttributes: this.attr('modifiedFields'),
      });
      this.attr('modifiedFields', {}, true);
    },
  }),
});
