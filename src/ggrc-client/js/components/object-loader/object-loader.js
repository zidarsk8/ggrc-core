/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import canMap from 'can-map';
import canComponent from 'can-component';
import RefreshQueue from '../../models/refresh_queue';
import {reify, isReifiable} from '../../plugins/utils/reify-utils';

export default canComponent.extend({
  tag: 'object-loader',
  leakSkope: true,
  viewModel: canMap.extend({
    define: {
      path: {
        set(value) {
          if (value && isReifiable(value)) {
            new RefreshQueue().enqueue(reify(value)).trigger().then(
              (response) => {
                this.attr('loadedObject', response[0]);
              });
          } else {
            this.attr('loadedObject', null);
          }
          return value;
        },
      },
    },
    loadedObject: null,
  }),
});
