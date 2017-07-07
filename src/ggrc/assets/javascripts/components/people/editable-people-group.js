/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, Mustache) {
  'use strict';

  var viewModel = GGRC.VM.DeletablePeopleGroup.extend({
    title: '@',
    editableMode: false,
    canEdit: {},
    personSelected: function (person) {
      this.dispatch({
        type: 'personSelected',
        person: person,
        groupId: this.attr('groupId')
      });
    },
    save: function () {
      this.dispatch('saveChanges');
    },
    cancel: function () {
      this.changeEditableMode(false);
    },
    changeEditableMode: function (editableMode) {
      this.attr('editableMode', editableMode);
      this.dispatch({
        type: 'changeEditableMode',
        isAddEditableGroup: editableMode,
        groupId: this.attr('groupId')
      });
    }
  });

  GGRC.Components('editablePeopleGroup', {
    tag: 'editable-people-group',
    template: can.view(
      GGRC.mustache_path +
      '/components/people/editable-people-group.mustache'
    ),
    viewModel: viewModel,
    events: {
      '{window} mousedown': function (el, ev) {
        var viewModel = this.viewModel;
        var editableIcon = $(ev.target).hasClass('set-editable-group');
        var isInside = GGRC.Utils.events.isInnerClick(this.element, ev.target);
        var editableMode = viewModel.attr('editableMode');

        if (!isInside && editableMode) {
          viewModel.save();
        }

        if (isInside && !editableMode && editableIcon) {
          viewModel.changeEditableMode(true);
        }
      }
    }
  });
})(window.can, window.GGRC, can.Mustache);
