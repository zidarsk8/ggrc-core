/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './questionnaire-mapping-link.stache';
import {
  getMappingUrl,
  getUnmappingUrl,
} from '../../plugins/utils/ggrcq-utils';

export default CanComponent.extend({
  tag: 'questionnaire-mapping-link',
  view: can.stache(template),
  leakScope: false,
  viewModel: CanMap.extend({
    define: {
      externalUrl: {
        get() {
          let instance = this.attr('instance');
          let destination = this.attr('destinationModel');

          switch (this.attr('type')) {
            case 'map': {
              return getMappingUrl(instance, destination);
            }
            case 'unmap': {
              return getUnmappingUrl(instance, destination);
            }
          }
        },
      },
    },
    instance: null,
    destinationModel: null,
    cssClasses: '',
    type: 'map',
  }),
});
