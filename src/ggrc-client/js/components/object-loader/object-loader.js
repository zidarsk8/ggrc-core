/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import CanMap from 'can-map';
import CanComponent from 'can-component';
import RefreshQueue from '../../models/refresh_queue';
import {reify, isReifiable} from '../../plugins/utils/reify-utils';

export default CanComponent.extend({
  tag: 'object-loader',
  leakSkope: true,
  viewModel: CanMap.extend({
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
