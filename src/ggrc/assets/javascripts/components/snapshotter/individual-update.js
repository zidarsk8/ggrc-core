/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, $) {
  'use strict';

  GGRC.Components('SnapshotIndividualUpdater', {
    tag: 'snapshot-individual-update',
    template: '<content/>',
    scope: {
      instance: null,
      updateIt: function (scope, el, ev) {
        GGRC.Controllers.Modals.confirm({
          instance: scope,
          modal_title: 'Update to latest version',
          modal_description:
            'Do you want to update this ' +
            this.instance.class.title_singular +
            ' version of the Audit to the latest version?',
          modal_confirm: 'Update',
          skip_refresh: true,
          button_view: GGRC.mustache_path + '/modals/prompt_buttons.mustache'
        }, function () {
          var instance = this.instance.snapshot;
          instance.refresh().then(function () {
            instance.attr('update_revision', 'latest');
            return instance.save();
          }).then(function () {
            window.location.reload();
          });
        }.bind(this));
      }
    }
  });
})(window.can, window.can.$);
