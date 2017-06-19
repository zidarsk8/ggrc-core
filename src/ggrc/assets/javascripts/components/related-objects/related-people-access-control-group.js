/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, _, GGRC, Permission, Mustache) {
  'use strict';

  GGRC.Components('relatedPeopleAccessControlGroup', {
    tag: 'related-people-access-control-group',
    viewModel: {
      instance: {},

      define: {
        // whether or not the instance is a new object that is yet to be
        // created on the backend
        isNewInstance: {
          type: 'boolean',
          value: false
        },

        // whether or not to automatically save instance on person role changes
        autosave: {
          type: 'boolean',
          value: false
        },

        // a flag indicating whether a user role modification is in progress
        isUpdating: {
          get: function () {
            return Boolean(this.attr('isPendingGrant') ||
                           this.attr('pendingRevoke') !== null);
          }
        }
      },
      groupId: '@',
      title: '@',
      people: [],
      isUpdating: false,
      canEdit: false,
      backUpAccessControlList: [],
      editableMode: false,
      isPendingGrant: false,

      refreshInstanceAfterCancel: function (groupId) {
        this.attr('editableMode', false);
        this.attr('instance.access_control_list')
          .replace(this.attr('backUpAccessControlList'));
        this.attr('instance').dispatch('refreshInstance');
      },
      // only one group can be editable
      changeEditableGroup: function (args) {
        var groupId = args.groupId;
        var isAddEditableGroup = args.isAddEditableGroup;

        if (isAddEditableGroup) {
          this.attr('editableMode', true);
        } else {
          this.refreshInstanceAfterCancel(groupId);
        }
      },
      saveChanges: function () {
        var self = this;
        this.attr('editableMode', false);
        this.attr('instance').save()
          .then(function () {
            self.attr('instance').dispatch('refreshInstance');
          })
      },
      personSelected: function (args) {
        this.addPerson(args.person, args.groupId);
      },
      addPerson: function (person, groupId) {
        this.grantRole(person, groupId);
      },
      removePerson: function (args) {
        var groupId = args.groupId;
        var person = args.person;

        this.revokeRole(person, groupId);
      },

      /**
       * Grant role to user on the model instance.
       *
       * If the user already has this role assigned on the model instance,
       * nothing happens.
       *
       * @param {CMS.Models.Person} person - the user to grant a role to
       * @param {Number} roleId - ID if the role to grant
       */
      grantRole: function (person, roleId) {
        var inst = this.instance;
        var roleEntry;

        if (this.attr('isUpdating')) {
          return;
        }

        this.attr('isPendingGrant', true);

        roleEntry = _.find(
          inst.attr('access_control_list'),
          {person: {id: person.id}, ac_role_id: roleId}
        );

        if (roleEntry) {
          console.warn(
            'User ', person.id, 'already has role', roleId, 'assigned');
          this.attr('isPendingGrant', false);
          return;
        }

        if (!inst.access_control_list) {
          inst.attr('access_control_list', []);
        }

        can.batch.start();
        roleEntry = {person: person, ac_role_id: roleId};
        inst.attr('access_control_list').push(roleEntry);

        if (!this.autosave) {
          this.attr('isPendingGrant', false);
          this._rebuildRolesInfo();
          can.batch.stop();
          return;
        }

        inst.save()
          .done(function () {
            GGRC.Errors.notifier('success', 'User role added.');
          })
          .fail(function () {
            GGRC.Errors.notifier('error', 'Adding user role failed.');
          })
          .always(function () {
            this.attr('isPendingGrant', false);
            this._rebuildRolesInfo();
            can.batch.stop();
          }.bind(this));
      },

      /**
       * Revoke role from user on the model instance.
       *
       * If the user already does not have this role assigned on the model
       * instance, nothing happens.
       *
       * @param {CMS.Models.Person} person - the user to grant a role to
       * @param {Number} roleId - ID if the role to grant
       */
      revokeRole: function (person, roleId) {
        var idx;
        var inst = this.instance;

        if (this.attr('isUpdating')) {
          return;
        }

        this.attr('pendingRevoke', [person.id, roleId]);

        idx = _.findIndex(
          inst.attr('access_control_list'),
          {person: {id: person.id}, ac_role_id: roleId}
        );

        if (idx < 0) {
          console.warn('Role ', roleId, 'not found for user', person.id);
          this.attr('pendingRevoke', null);
          return;
        }

        can.batch.start();
        inst.access_control_list.splice(idx, 1);

        if (!this.autosave) {
          this.attr('pendingRevoke', null);
          this._rebuildRolesInfo();
          can.batch.stop();
          return;
        }

        inst.save()
          .done(function () {
            GGRC.Errors.notifier('success', 'User role removed.');
          })
          .fail(function () {
            GGRC.Errors.notifier('error', 'Removing user role failed.');
          })
          .always(function () {
            this.attr('pendingRevoke', null);
            this._rebuildRolesInfo();
            can.batch.stop();
          }.bind(this));
      },

      _rebuildRolesInfo: function () {
        var self = this;
        var instance = this.instance;
        var list = instance.access_control_list;
        var currentGroup = list ?
          list.filter(function (item) {
            return item.ac_role_id == self.attr('groupId');
          }) :
          [];

        var people = currentGroup.map(function (item) {
          return item.person;
        });

        this.attr('people').replace(people);
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
        var canEdit;
        var vm = this.viewModel;
        var instance = vm.instance;
        var isSnapshot;

        if (!instance) {
          console.error('accessControlList component: instance not given.');
          return;
        }

        isSnapshot = GGRC.Utils.Snapshots.isSnapshot(instance);
        canEdit = !isSnapshot &&  // snapshots are not editable
                  (vm.isNewInstance ||
                   Permission.is_allowed_for('update', instance));

        can.batch.start();
        vm.attr('canEdit', canEdit);
        vm.attr('isPendingGrant', false);

         // which [personId, roleId] combination is currently being revoked
        vm.attr('pendingRevoke', null);

        vm.attr('_rolesInfoFixed', false);
        vm._rebuildRolesInfo();
        can.batch.stop();

        vm.attr('backUpAccessControlList').replace(vm.instance.access_control_list);
      },

      '{viewModel.instance.access_control_list} change':
      function (context, ev, index, how, newVal, oldVal) {
        if (how === 'set') {
          // we are not interested in collection items' changes, all we care
          // about is ading and removing role assignments
          return;
        }

        this.viewModel._rebuildRolesInfo();
      },

      // FIXME: For some reson the rolesInfo object might get corrupted and
      // needs to be manually checked for consistency and fixed if needed. Not
      // an elegant approach, but it works.
      '{viewModel.rolesInfo} change': function () {
        var vm = this.viewModel;
        var fixNeeded = false;

        if (vm.attr('_rolesInfoFixed')) {
          // It seems that once the roleInfo object is fixed, the issue does
          // not occur anymore, thus fixing the object only once suffices.
          return;
        }

        vm.attr('rolesInfo').forEach(function (item) {
          var roleId = item.role.id;

          if (!item.roleAssignments) {
            return;
          }

          item.roleAssignments.forEach(function (entry) {
            if (entry.ac_role_id !== roleId) {
              fixNeeded = true;
            }
          });
        });

        if (fixNeeded) {
          vm.attr('_rolesInfoFixed', true);
          console.warn('accessControlList: Need TO fix rolesInfo');
          vm._rebuildRolesInfo();
        }
      }
    }
  });
})(window.can, window._, window.GGRC, window.Permission, can.Mustache);
