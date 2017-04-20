/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can) {
  'use strict';

  var tag = 'folder-attachments-list';
  var template = can.view(GGRC.mustache_path +
    '/components/folder-attachments-list/folder-attachments-list.mustache');

  /**
   * Wrapper Component for rendering and managing of folder and
   * attachments lists
   */
  GGRC.Components('folderAttachmentsList', {
    tag: tag,
    template: template,
    viewModel: {
      define: {
        denyNoFolder: {
          type: 'boolean',
          value: false
        }
      },
      title: '@',
      tooltip: '@',
      subLabel: '@',
      instance: null,
      readonlyFolder: function () {
        return this.attr('instance.isRevision') ||
               this.attr('instance.snapshot');
      }
    },
    events: {
      init: function () {}
    }
  });
})(window.GGRC, window.can);
