/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, _, GGRC, Permission, Mustache) {
  'use strict';

  /**
   * A component that renders a list of access permissions granted on the given
   * instance of a roleable model.
   *
   * Permissions are goruped by their access control role type and can be
   * edited by users.
   */
  GGRC.Components('accessControlList', {
    tag: 'access-control-list',
    template: can.view(
      GGRC.mustache_path +
      '/components/access_control_list/access_control_list.mustache'
    ),

    viewModel: {
      instance: null,

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

        // the extra CSS class(es) to apply to the main container element
        topWrapperClass: {
          type: 'string',
          value: 'span12'
        },

        // the extra CSS class(es) to apply to each role list block
        roleBlockClass: {
          type: 'string',
          value: 'row-fluid'
        },

        // a flag indicating whether a user role modification is in progress
        isUpdating: {
          get: function () {
            return Boolean(this.attr('isPendingGrant') ||
                           this.attr('pendingRevoke') !== null);
          }
        }
      },

      /**
       * Enter the "grant role" mode for a particular role.
       *
       * It effectively displays the UI widget for granting a person that role.
       *
       * @param {Number} roleId - the role ID for which to enable the "grant
       *   role" mode
       */
      grantRoleMode: function (roleId) {
        if (this.attr('isUpdating')) {
          return;
        }

        this.attr('grantingRoleId', roleId);
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
        roleEntry = {
          person: {
            id: person.id,
            type: person.type
          },
          ac_role_id: roleId
        };
        inst.attr('access_control_list').push(roleEntry);

        if (!this.autosave) {
          this.attr('grantingRoleId', 0);
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
            this.attr('grantingRoleId', 0);
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

      /**
       * Update the role info object used by the template to display the roles
       * and the users which have them granted.
       */
      _rebuildRolesInfo: function () {
        var roleAssignments;
        var roles;
        var rolesInfo;
        var instance = this.instance;

        if (!instance) {
          this.attr('rolesInfo', []);
          return;
        }

        roleAssignments = _.groupBy(instance.access_control_list, 'ac_role_id');

        roles = _.filter(GGRC.access_control_roles, {
          object_type: instance.class.model_singular
        });
        rolesInfo = _.map(roles, function (role) {
          return {role: role, roleAssignments: roleAssignments[role.id]};
        });

        this.attr('rolesInfo', rolesInfo);
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
                   Permission.is_allowed_for('update', instance)) &&
                  !instance.archived;

        can.batch.start();
        vm.attr('canEdit', canEdit);
        vm.attr('grantingRoleId', 0);  // which "add role" autocomplete to show
        vm.attr('isPendingGrant', false);

         // which [personId, roleId] combination is currently being revoked
        vm.attr('pendingRevoke', null);

        vm.attr('_rolesInfoFixed', false);
        vm._rebuildRolesInfo();
        can.batch.stop();
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
    },
    helpers: {
      /**
       * Check if the role is currently being revoked from the person and render
       * the corresponding template block.
       *
       * @param {Number} personId - the ID of the person
       * @param {Number} roleId - the ID of the role to check
       * @param {Object} options - the Mustache options object
       *
       * @return {String} - the rendered template block
       */
      ifRevokingRole: function (personId, roleId, options) {
        var pendingRevoke = this.attr('pendingRevoke');

        if (pendingRevoke === null) {
          return options.inverse();
        }

        personId = Mustache.resolve(personId);
        roleId = Mustache.resolve(roleId);

        if (pendingRevoke[0] === personId && pendingRevoke[1] === roleId) {
          return options.fn();
        }
        return options.inverse();
      }
    }
  });
})(window.can, window._, window.GGRC, window.Permission, can.Mustache);
