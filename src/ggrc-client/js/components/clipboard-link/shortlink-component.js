/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
import './clipboard-link';

export default CanComponent.extend({
  tag: 'shortlink-component',
  view: can.stache(
    '<clipboard-link text:from="text">' +
    '<i class="fa fa-google"/>Get Short Url</clipboard-link>'
  ),
  leakScope: true,
  viewModel: CanMap.extend({
    instance: null,
    define: {
      text: {
        type: String,
        get() {
          let instance = this.attr('instance');
          let prefix = GGRC.config.ASSESSMENT_SHORT_URL_PREFIX;
          if (prefix && !prefix.endsWith('/')) {
            prefix += '/';
          }

          return (prefix && instance.id) ? `${prefix}${instance.id}` : '';
        },
      },
    },
  }),
});
