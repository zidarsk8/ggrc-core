/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, Mustache) {
  'use strict';

  GGRC.Components('editablePeopleGroup', {
    tag: 'editable-people-group',
    template: can.view(
      GGRC.mustache_path +
      '/components/people/editable-people-group.mustache'
    ),
    viewModel: {
      define: {
        peopleLength: {
          get: function () {
            return this.attr('people').length;
          }
        },
        emptyListMessage: {
          type: 'string',
          value: ''
        }
      },
      title: '@',
      required: '@',
      people: [],
      groupId: '@',
      instance: {},
      isLoading: false,
      canUnmap: true,
      withDetails: false,
      editableMode: false,
      validation: {},
      personSelected: function (person) {
        this.dispatch({
          type: 'personSelected',
          person: person,
          groupId: this.attr('groupId')
        });
      },
      unmap: function (person) {
        this.dispatch({
          type: 'unmap',
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
    },
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
