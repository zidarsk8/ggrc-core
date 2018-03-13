/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import '../../components/advanced-search/advanced-search-filter-container';
import '../../components/advanced-search/advanced-search-filter-state';
import '../../components/advanced-search/advanced-search-wrapper';
import '../../components/unified-mapper/mapper-results';
import '../../components/collapsible-panel/collapsible-panel';
import './bulk-update-target-state';
import {getBulkStatesForModel} from '../../plugins/utils/state-utils';
import ObjectOperationsBaseVM from '../view-models/object-operations-base-vm';
import template from './object-bulk-update.mustache';
import tracker from '../../tracker';

export default can.Component.extend({
  tag: 'object-bulk-update',
  template: template,
  viewModel: function (attrs, parentViewModel) {
    let type = attrs.type;
    let targetStates = getBulkStatesForModel(type);
    let targetState = targetStates.length ? targetStates[0] : null;

    return ObjectOperationsBaseVM.extend({
      type: attrs.type,
      object: attrs.object,
      availableTypes: function () {
        let object = this.attr('object');
        let type = GGRC.Mappings.getMappingType(object);
        return type;
      },
      reduceToOwnedItems: true,
      showTargetState: true,
      targetStates: targetStates,
      targetState: targetState,
      callback: parentViewModel.attr('callback'),
    });
  },
  events: {
    closeModal: function () {
      if (this.element) {
        this.element.find('.modal-dismiss').trigger('click');
      }
    },
    '.btn-cancel click': function () {
      this.closeModal();
    },
    '.btn-update click': function () {
      let callback = this.viewModel.callback;
      const stopFn = tracker.start(
        this.viewModel.attr('type'),
        tracker.USER_JOURNEY_KEYS.LOADING,
        tracker.USER_ACTIONS.CYCLE_TASK.BULK_UPDATE);

      callback(this, {
        selected: this.viewModel.attr('selected'),
        options: {
          state: this.viewModel.attr('targetState'),
        },
      }).then(stopFn, stopFn.bind(null, true));
    },
  },
});
