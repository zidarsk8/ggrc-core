/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  'use strict';

  GGRC.Components('openOriginalLink', {
    tag: 'open-original-link',
    template: can.view(
      GGRC.mustache_path +
      '/snapshots/open_original_link.mustache'
    ),
    viewModel: {
      originalDeleted: false,
      define: {
        revisions: {
          set: function (value) {
            var lastRevision;

            if (!value || value.length === 0) {
              return;
            }

            lastRevision = value[value.length - 1];
            this.checkOriginal(lastRevision.id);
          }
        }
      },
      checkOriginal: function (revisionId) {
        var self = this;
        var queryAPI = GGRC.Utils.QueryAPI;
        var filter = {
          expression: {
            op: {name: '='},
            left: 'id',
            right: revisionId
          }
        };

        var params = queryAPI.buildParam(
          'Revision', {}, undefined, undefined, filter);

        queryAPI.makeRequest({data: [params]})
          .then(function (response) {
            var revision = response[0].Revision;

            if (revision.count > 0) {
              self.attr('originalDeleted',
                revision.values[0].action === 'deleted');
            }
          }
        );
      }
    }
  });
})(window.can, window.can.$);
