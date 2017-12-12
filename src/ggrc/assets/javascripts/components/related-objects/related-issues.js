/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import './related-objects';
import '../add-issue-button/add-issue-button';

(function (can, GGRC) {
  'use strict';
  var tpl = can.view(GGRC.mustache_path +
    '/components/related-objects/related-issues.mustache');

  GGRC.Components('relatedIssues', {
    tag: 'related-issues',
    template: tpl,
    viewModel: {
      define: {
        orderBy: {
          type: 'string',
          value: 'created_at'
        },
        allRelatedSnapshots: {
          Value: can.List
        },
        itemsType: {
          type: 'string',
          value: 'Issue'
        },
        relatedIssuesFilter: {
          type: '*',
          get: function () {
            var id = this.attr('baseInstance.id');
            var type = this.attr('baseInstance.type');
            return {
              expression: {
                left: {
                  object_name: type,
                  op: {name: 'relevant'},
                  ids: [id]
                },
                right: {
                  object_name: type,
                  op: {name: 'similar'},
                  ids: [id]
                },
                op: {name: 'OR'}
              }
            };
          }
        }
      },
      baseInstance: null
    }
  });
})(window.can, window.GGRC);
