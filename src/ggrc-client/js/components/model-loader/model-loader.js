/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './model-loader.stache';

export default CanComponent.extend({
  tag: 'model-loader',
  view: can.stache(template),
  leakScope: true,
  viewModel: CanMap.extend({
    define: {
      loadedModel: {
        get(last, set) {
          let path = this.attr('path');
          import(`../../models/${path}`).then((model) => set(model.default));
        },
      },
    },
    path: '',
  }),
});
