/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import canStache from 'can-stache';
import canMap from 'can-map';
import CanComponent from 'can-component';
import template from './spinner-component.stache';

export default CanComponent.extend({
  tag: 'spinner-component',
  view: canStache(template),
  leakScope: true,
  scope: canMap.extend({
    extraCssClass: '',
    size: '',
    toggle: null,
  }),
});
