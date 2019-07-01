/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import loIdentity from 'lodash/identity';
import canMap from 'can-map';
import canComponent from 'can-component';
import {
  confirm,
  BUTTON_VIEW_CONFIRM_CANCEL,
} from '../../plugins/utils/modals';
import {
  refreshCounts,
} from '../../plugins/utils/widgets-utils';
import {notifier} from '../../plugins/utils/notifiers-utils';
import pubSub from '../../pub-sub';
import {trigger} from 'can-event';

export default canComponent.extend({
  tag: 'snapshot-scope-update',
  leakScope: false,
  viewModel: canMap.extend({
    instance: null,
    upsertIt: function (scope, el, ev) {
      confirm({
        instance: scope.instance,
        modal_title: 'Update to latest version',
        modal_description:
          'Do you want to update all objects of this Audit' +
          ' to the latest version?',
        modal_confirm: 'Update',
        button_view: BUTTON_VIEW_CONFIRM_CANCEL,
        skip_refresh: true,
      },
      this._success.bind(this),
      this._dismiss.bind(this)
      );
    },
    _refreshContainers: function () {
      pubSub.dispatch({
        type: 'refetchOnce',
        modelNames: GGRC.config.snapshotable_objects,
      });
      return refreshCounts();
    },
    _success: function () {
      let instance = this.instance;

      this._showProgressWindow();
      return instance
        .refresh()
        .then(function () {
          let data = {
            operation: 'upsert',
          };
          instance.attr('snapshots', data);
          return instance.save();
        })
        .then(this._refreshContainers.bind(this))
        .then(() => {
          this._updateVisibleContainer();
          this._showSuccessMsg();
          instance.dispatch('snapshotScopeUpdated');
        });
    },
    _dismiss: loIdentity,
    _showProgressWindow: function () {
      let message =
        'Audit refresh is in progress. This may take several minutes.';

      notifier('progress', message);
    },
    _updateVisibleContainer: function () {
      let visibleContainer = $('tree-widget-container:visible');
      if (visibleContainer.length === 0) {
        return;
      }
      // if a user switches to the snapshot tab during the audit refresh
      // then update the tab
      trigger.call(visibleContainer[0], 'refreshTree');
    },
    _showSuccessMsg: function () {
      let message = 'Audit was refreshed successfully.';
      $('alert-progress').remove();
      notifier('success', message);
    },
  }),
});
