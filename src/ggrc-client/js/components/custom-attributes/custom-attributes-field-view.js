/*
   Copyright (C) 2019 Google Inc.
   Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import '../inline/readonly-inline-content';
import '../form/field-views/checkbox-form-field-view';
import '../form/field-views/date-form-field-view';
import '../form/field-views/person-form-field-view';
import '../form/field-views/text-form-field-view';
import template from './custom-attributes-field-view.stache';

export default CanComponent.extend({
  tag: 'custom-attributes-field-view',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    type: null,
    value: null,
  }),
});
