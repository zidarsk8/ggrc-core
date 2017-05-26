/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can) {
  'use strict';

  var tag = 'cycle-task-entry-attach-button';
  var template = can.view(GGRC.mustache_path +
    '/cycle_task_entries/attach-button.mustache');

  GGRC.Components('cycleTaskEntryAttachButton', {
    tag: tag,
    template: template,
    viewModel: {
      updatedCallback: '@',
      parentInstance: null,
      itemsUploadedCallback: function () {
        if (_.isFunction(this.attr('updatedCallback'))) {
          this.attr('updatedCallback')();
        }
      }
    }
  });
})(window.GGRC, window.can);
