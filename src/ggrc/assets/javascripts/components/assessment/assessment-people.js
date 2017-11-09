/*
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

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
          value: '',
        },
      },
      rolesConflict: false,
      infoPaneMode: true,
      withDetails: false,
      instance: {},
      conflictRoles: ['Assignees', 'Verifiers'],
      orderOfRoles: ['Creators', 'Assignees', 'Verifiers'],
    },
    events: {
      '{instance} rolesConflict': function (ev, args) {
        this.viewModel.attr('rolesConflict', args.rolesConflict);
      },
    },
  });
})(window.can, window.GGRC);
