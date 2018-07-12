/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {
  initCounts,
} from '../../plugins/utils/current-page-utils';

/**
 * A component that wraps a button for ending a Workflow cycle, and
 * automatically handles a click on it.
 *
 * As a result, the Cycle instance passed to the component is ended, and
 * a couple of affected objects are refreshed in the process.
 *
 * Usage example (state and permission checks not included):
 *
 *   <cycle-end-cycle cycle="instance">
 *       <button>Click to end a Cycle</button>
 *   </cycle-end-cycle>
 *
 */
(function (GGRC, can) {
  'use strict';

  GGRC.Components('endCycleButtonWrap', {
    tag: 'cycle-end-cycle',
    template: '<content/>',
    events: {
      click: function (el, ev) {
        ev.stopPropagation();

        this.scope.cycle
          .refresh()
          .then(function (cycle) {
            return cycle.attr('is_current', false).save();
          })
          .then(function () {
            return GGRC.page_instance().refresh();
          })
          .then(function () {
            let pageInstance = GGRC.page_instance();
            let WorkflowExtension =
              GGRC.extensions.find(function (extension) {
                return extension.name === 'workflows';
              });

            can.trigger(el, 'refreshTree');

            return initCounts([
              WorkflowExtension.countsMap.history,
            ],
            pageInstance.type,
            pageInstance.id);
          }.bind(this));
      },
    },
  });
})(window.GGRC, window.can);
