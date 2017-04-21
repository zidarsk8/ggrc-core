/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can) {
  'use strict';

  var tag = 'assessment-attachments-list';
  var template = can.view(GGRC.mustache_path +
    '/components/assessment/attachments-list.mustache');

  /**
   * Wrapper Component for rendering and managing of attachments lists
   */
  GGRC.Components('assessmentAttachmentsList', {
    tag: tag,
    template: template,
    viewModel: {
      define: {
        noItemsText: {
          type: 'string',
          value: ''
        }
      },
      title: '@',
      tooltip: '@',
      limit: 5
    }
  });
})(window.GGRC, window.can);
