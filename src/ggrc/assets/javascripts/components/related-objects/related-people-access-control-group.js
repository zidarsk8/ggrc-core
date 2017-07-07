/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, _, GGRC, Permission) {
  'use strict';

  GGRC.Components('relatedPeopleAccessControlGroup', {
    tag: 'related-people-access-control-group',
    viewModel: {
      define: {
        canEdit: {
          get: function () {
            var instance = this.attr('instance');
            var isSnapshot = GGRC.Utils.Snapshots.isSnapshot(instance);
            var canEdit = !isSnapshot &&
              !this.attr('updatableGroupId') &&
              (this.attr('isNewInstance') ||
                Permission.is_allowed_for('update', instance));

            return canEdit;
          }
        },
        isLoading: {
          get: function () {
            return this.attr('updatableGroupId') ===
              this.attr('groupId');
          }
        }
      },
      instance: {},
      isNewInstance: false,
      groupId: '@',
      title: '@',
      people: [],
      editableMode: false,
      isDirty: false,
      required: false,
      backUpPeople: [],
      infoPaneMode: true,
      updatableGroupId: null,

      refreshInstanceAfterCancel: function (groupId) {
        this.attr('editableMode', false);
        this.attr('isDirty', false);
        this.attr('people').replace(this.attr('backUpPeople'));
      },
      // only one group can be editable
      changeEditableGroup: function (args) {
        var groupId = args.groupId;
        var isAddEditableGroup = args.isAddEditableGroup;

        if (isAddEditableGroup) {
          this.attr('editableMode', true);
          this.attr('backUpPeople')
            .replace(this.attr('people'));
        } else {
          this.refreshInstanceAfterCancel(groupId);
        }
      },
      saveChanges: function () {
        this.attr('editableMode', false);

        if (this.attr('isDirty')) {
          this.attr('isDirty', false);
          this.dispatch({
            type: 'saveRoles',
            people: this.attr('people'),
            roleId: this.attr('groupId')
          });
        }
      },
      personSelected: function (args) {
        this.addPerson(args.person, args.groupId);
      },
      addPerson: function (person, groupId) {
        var exist = _.find(
          this.attr('people'),
          {id: person.id}
        );

        if (exist) {
          console.warn('User ', person.id,
            'already has role', groupId, 'assigned');
          return;
        }

        this.attr('isDirty', true);
        this.attr('people').push(person);

        // Don't dispatch add role if NOT modal mode
        if (this.attr('infoPaneMode')) {
          return;
        }

        this.dispatch({
          type: 'addRole',
          person: person,
          groupId: groupId
        });
      },
      removePerson: function (args) {
        var groupId = args.groupId;
        var person = args.person;
        var idx = _.findIndex(
          this.attr('people'),
          {id: person.id});

        this.attr('isDirty', true);
        this.attr('people').splice(idx, 1);

        // Don't dispatch add role if NOT modal mode
        if (this.attr('infoPaneMode')) {
          return;
        }

        this.dispatch({
          type: 'removeRole',
          person: person,
          groupId: groupId
        });
      }
    },
    events: {
      /**
       * The component entry point.
       *
       * @param {jQuery} $element - the DOM element that triggered
       *   creating the component instance
       * @param {Object} options - the component instantiation options
       */
      init: function ($element, options) {
        var vm = this.viewModel;
        var instance = vm.attr('instance');
        if (!instance) {
          console.error('accessControlList component: instance not given.');
          return;
        }

        vm.attr('backUpPeople').replace(vm.attr('people'));
      }
    }
  });
})(window.can, window._, window.GGRC, window.Permission);
