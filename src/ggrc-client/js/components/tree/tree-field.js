/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
import template from './templates/tree-field.stache';
import {getTruncatedList} from '../../plugins/ggrc_utils';

export default CanComponent.extend({
  tag: 'tree-field',
  view: can.stache(template),
  viewModel: CanMap.extend({
    define: {
      tooltipContent: {
        get() {
          let source = this.attr('source');
          return getTruncatedList(source);
        },
      },
    },
    showTooltip: true,
    source: [],
  }),
});
