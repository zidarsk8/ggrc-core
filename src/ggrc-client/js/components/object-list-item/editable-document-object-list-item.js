/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import canStache from 'can-stache';
import canMap from 'can-map';
import CanComponent from 'can-component';
import '../object-list-item/document-object-list-item';
import template from './editable-document-object-list-item.stache';

export default CanComponent.extend({
  tag: 'editable-document-object-list-item',
  view: canStache(template),
  leakScope: true,
  viewModel: canMap.extend({
    document: {},
  }),
});
