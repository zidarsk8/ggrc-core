/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../people/deletable-people-group';
import '../people/editable-people-group';
import '../related-objects/related-people-mapping';
import '../related-objects/related-people-access-control';
import '../related-objects/related-people-access-control-group';
import '../custom-roles/custom-roles';
import '../custom-roles/custom-roles-modal';

(function (can, GGRC) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/assessment-people.mustache');
  var tag = 'assessment-people';

  can.Component.extend({
    tag: tag,
    template: tpl,
    viewModel: {
      define: {
        emptyMessage: {
          type: 'string',
          value: ''
        }
      },
      infoPaneMode: true,
      withDetails: false,
      instance: {}
    }
  });
})(window.can, window.GGRC);
