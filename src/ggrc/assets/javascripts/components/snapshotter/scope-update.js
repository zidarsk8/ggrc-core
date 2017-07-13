/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (GGRC, can, $) {
  'use strict';

  var snapshotModels = [
    'AccessGroup',
    'Clause',
    'Contract',
    'Control',
    'DataAsset',
    'Facility',
    'Market',
    'Objective',
    'OrgGroup',
    'Policy',
    'Process',
    'Product',
    'Regulation',
    'Risk',
    'Section',
    'Standard',
    'System',
    'Threat',
    'Vendor'
  ];

  GGRC.Components('SnapshotScopeUpdater', {
    tag: 'snapshot-scope-update',
    template: '<content/>',
    scope: {
      instance: null,
      snapshotModels: snapshotModels,
      upsertIt: function (scope, el, ev) {
        GGRC.Controllers.Modals.confirm({
          instance: scope.instance,
          modal_title: 'Update to latest version',
          modal_description:
            'Do you want to update all objects of this Audit' +
            ' to the latest version?',
          modal_confirm: 'Update',
          button_view: GGRC.Controllers.Modals.BUTTON_VIEW_OK_CLOSE,
          skip_refresh: true
        },
          this._success.bind(this),
          this._dismiss.bind(this)
        );
      },
      _refreshContainers: function () {
        var modelNames = this.snapshotModels;

        GGRC.Utils.CurrentPage.refreshCounts();

        // tell each container with snapshots that it should refresh own data
        $('tree-widget-container')
          .each(function () {
            var vm = $(this).viewModel();
            var modelName = vm.model.model_singular;

            if (!_.includes(modelNames, modelName)) {
              return true;
            }

            vm.setRefreshFlag(true);
          });
      },
      _success: function () {
        var instance = this.instance;

        this._showProgressWindow();
        instance
          .refresh()
          .then(function () {
            var data = {
              operation: 'upsert'
            };
            instance.attr('snapshots', data);
            return instance.save();
          })
          .then(this._refreshContainers.bind(this))
          .then(this._updateVisibleContainer.bind(this))
          .then(this._showSuccessMsg.bind(this));
      },
      _dismiss: _.identity,
      _showProgressWindow: function () {
        var message =
          'Audit refresh is in progress. This may take several minutes.';

        GGRC.Errors.notifier('progress', [message]);
      },
      _updateVisibleContainer: function () {
        var visibleContainer = $('tree-widget-container:visible');
        var FORCE_REFRESH = true;
        if (visibleContainer.length === 0) {
          return;
        }
        // if a user switches to the snapshot tab during the audit refresh
        // then update the tab
        visibleContainer.viewModel().display(FORCE_REFRESH);
      },
      _showSuccessMsg: function () {
        var message = 'Audit has refreshed successfully.';
        $('alert-progress').remove();
        GGRC.Errors.notifier('success', [message]);
      }
    }
  });
})(GGRC, window.can, window.can.$);
