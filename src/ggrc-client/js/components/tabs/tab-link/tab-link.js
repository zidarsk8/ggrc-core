/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
const viewModel = CanMap.extend({
  tabType: 'link',
  instance: null,
  titleText: '',
  linkType: '',
  panels: [],
  setupPanels() {
    this.attr('panels').push(this);
    this.attr('panels').dispatch('panelAdded');
  },
});

export default CanComponent.extend({
  tag: 'tab-link',
  leakScope: true,
  viewModel,
  events: {
    inserted() {
      this.viewModel.setupPanels();
    },
  },
});
