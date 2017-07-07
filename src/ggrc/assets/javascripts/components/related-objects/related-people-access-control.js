/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, _, GGRC) {
  'use strict';

  GGRC.Components('relatedPeopleAccessControl', {
    tag: 'related-people-access-control',
    viewModel: {
      instance: {},
      includeRoles: [],
      groups: [],
      updatableGroupId: null,
      infoPaneMode: true,
      isNewInstance: false,
      autosave: false,

      saveRoles: function (args) {
        var self = this;
        var people = args.people;
        var roleId = args.roleId;
        this.attr('updatableGroupId', roleId);

        this.updateAccessContolList(people, roleId);

        this.attr('instance').save()
          .then(function () {
            self.attr('instance').dispatch('refreshInstance');
            self.attr('updatableGroupId', null);
            self.attr('groups', self.getRoleList());
          });
      },
      updateAccessContolList: function (people, roleId) {
        var instance = this.attr('instance');

        // remove all people with current role
        var listWithoutRole = instance
          .attr('access_control_list').filter(function (item) {
            return item.ac_role_id !== roleId;
          });

        // push update people with current role
        people.forEach(function (person) {
          listWithoutRole.push({
            ac_role_id: roleId,
            person: {id: person.id, type: 'Person'}
          });
        });

        instance.attr('access_control_list')
          .replace(listWithoutRole);
      },
      addPerson: function (args) {
        var person = args.person;
        var groupId = args.groupId;

        this.grantRole(person, groupId);
      },
      removePerson: function (args) {
        var person = args.person;
        var groupId = args.groupId;

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
        var roleEntry;

        if (this.attr('updatableGroupId')) {
          return;
        }

        this.attr('updatableGroupId', roleId);

        roleEntry = _.find(
          this.attr('instance.access_control_list'),
          {person: {id: person.id}, ac_role_id: roleId}
        );

        if (roleEntry) {
          console.warn(
            'User ', person.id, 'already has role', roleId, 'assigned');
          this.attr('updatableGroupId', null);
          return;
        }

        if (!this.attr('instance.access_control_list')) {
          this.attr('instance.access_control_list', []);
        }

        can.batch.start();
        roleEntry = {
          person: {id: person.id, type: 'Person'},
          ac_role_id: roleId};
        this.attr('instance.access_control_list').push(roleEntry);

        this._save(true);
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

        if (this.attr('updatableGroupId')) {
          return;
        }

        this.attr('updatableGroupId', roleId);

        idx = _.findIndex(
          this.attr('instance.access_control_list'),
          {person: {id: person.id}, ac_role_id: roleId}
        );

        if (idx < 0) {
          console.warn('Role ', roleId, 'not found for user', person.id);
          this.attr('updatableGroupId', null);
          return;
        }

        can.batch.start();
        this.attr('instance.access_control_list').splice(idx, 1);

        this._save();
      },

      buildGroups: function (role, roleAssignments) {
        var includeRoles = this.attr('includeRoles');
        var groupId = role.id;
        var title = role.name;
        var group;
        var people;

        if (includeRoles.length && includeRoles.indexOf(title) === -1) {
          return;
        }

        group = roleAssignments[groupId];
        people = group ?
          group.map(function (groupItem) {
            return {
              id: groupItem.person.id,
              type: 'Person'
            };
          }) :
          [];

        return {
          title: title,
          groupId: groupId,
          people: people,
          required: role.mandatory
        };
      },
      getRoleList: function () {
        var roleAssignments;
        var roles;
        var groups;
        var instance = this.attr('instance');

        if (!instance) {
          this.attr('rolesInfo', []);
          return;
        }

        roleAssignments = _.groupBy(instance
          .attr('access_control_list'), 'ac_role_id');

        roles = _.filter(GGRC.access_control_roles, {
          object_type: instance.class.model_singular
        });

        groups = _.map(roles, function (role) {
          return this.buildGroups(role, roleAssignments);
        }.bind(this))
        .filter(function (group) {
          return typeof group !== 'undefined';
        })
        // sort by required
        .sort(function (a, b) {
          if (a.required === b.required) {
            return 0;
          }

          return a.required ? -1 : 1;
        });

        return groups;
      },
      _save: function (isAdding) {
        var successMessage = 'User role ' +
          (isAdding ? 'added.' : 'removed.');
        var errorMessage = isAdding ? 'Adding' : 'Removing' +
          ' user role failed.';

        if (!this.autosave) {
          this.attr('updatableGroupId', null);
          can.batch.stop();
          return;
        }

        this.attr('instance').save()
          .done(function () {
            GGRC.Errors.notifier('success', successMessage);
          })
          .fail(function () {
            GGRC.Errors.notifier('error', errorMessage);
          })
          .always(function () {
            this.attr('updatableGroupId', null);
            can.batch.stop();
          }.bind(this));
      }
    },
    events: {
      inserted: function () {
        this.viewModel.attr('groups',
          this.viewModel.getRoleList());
      },
      '{viewModel.instance.access_control_list} change':
      function () {
        this.viewModel.attr('groups', this.viewModel.getRoleList());
      }
    }
  });
})(window.can, window._, window.GGRC);
