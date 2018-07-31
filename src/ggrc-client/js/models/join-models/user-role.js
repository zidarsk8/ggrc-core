/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Join from './join';
import Role from '../service-models/role';
import Person from '../business-models/person';

export default Join('CMS.Models.UserRole', {
  root_object: 'user_role',
  root_collection: 'user_roles',
  findAll: 'GET /api/user_roles',
  update: 'PUT /api/user_roles/{id}',
  create: 'POST /api/user_roles',
  destroy: 'DELETE /api/user_roles/{id}',
  attributes: {
    context: 'CMS.Models.Context.stub',
    modified_by: 'CMS.Models.Person.stub',
    person: 'CMS.Models.Person.stub',
    role: 'CMS.Models.Role.stub',
  },
  join_keys: {
    person: Person,
    role: Role,
  },
}, {
  save: function () {
    let role;
    let _super = this._super;

    if (this.role && !this.role_name) {
      return _super.apply(this, arguments);
    }

    role = _.find(Role.cache, {name: this.role_name});
    if (role) {
      this.attr('role', role.stub());
      return _super.apply(this, arguments);
    }
    return Role.findAll({
      name__in: this.role_name,
    }).then(function (role) {
      if (!role.length) {
        return new $.Deferred().reject('Role not found');
      }
      role = role[0];
      this.attr('role', role.stub());
      return _super.apply(this, arguments);
    }.bind(this));
  },
});
