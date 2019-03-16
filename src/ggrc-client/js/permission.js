/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import {getPageInstance} from './plugins/utils/current-page-utils';
import Stub from '../js/models/stub';
import {getInstance} from '../js/plugins/utils/models-utils';
import {reify} from '../js/plugins/utils/reify-utils';

let ADMIN_PERMISSION;
let _CONDITIONS_MAP = {
  contains: function (instance, args) {
    let value = Permission._resolve_permission_variable(args.value);
    let listValue = instance[args.list_property] || [];
    let i;
    for (i = 0; i < listValue.length; i++) {
      if (listValue[i].id === value.id) {
        return true;
      }
    }
    return false;
  },
  is: function (instance, args) {
    let value = Permission._resolve_permission_variable(args.value);
    let propertyValue = _.reduce(args.property_name.split('.'),
      function (obj, key) {
        let value = obj.attr(key);
        if (value instanceof Stub) {
          value = reify(value);
        }
        return value;
      }, instance);
    return value === propertyValue;
  },
  'in': function (instance, args) {
    let value = Permission._resolve_permission_variable(args.value);
    let propertyValue = instance[args.property_name];
    if (propertyValue instanceof Stub) {
      propertyValue = reify(propertyValue);
    }
    return value.indexOf(propertyValue) >= 0;
  },
  forbid: function (instance, args, action) {
    let blacklist = args.blacklist[action] || [];
    return blacklist.indexOf(instance.type) < 0;
  },
  has_changed: function (instance, args) {
    return (instance.attr(args.property_name) === args.prevent_if);
  },
  has_not_changed: function (instance, args) {
    return !(instance.attr(args.property_name) === args.prevent_if);
  },
};
let permissionsCompute = can.compute(GGRC.permissions);

const Permission = can.Construct({
  _admin_permission_for_context: function (contextId) {
    return new Permission(
      ADMIN_PERMISSION.action, ADMIN_PERMISSION.resource_type, contextId);
  },

  _all_resource_permission: function (permission) {
    return new Permission(
      permission.action, ADMIN_PERMISSION.resource_type, permission.context_id);
  },

  _permission_match: function (permissions, permission) {
    let resourceTypes = permissions[permission.action] || {};
    let resourceType = resourceTypes[permission.resource_type] || {};
    let contexts = resourceType.contexts || [];

    return (contexts.indexOf(permission.context_id) > -1);
  },

  _is_allowed: function (permissions, permission) {
    if (!permissions) {
      return false; // ?
    }
    if (this._permission_match(
      permissions,
      new Permission(
        permission.action,
        permission.resource_type, null))) {
      return true;
    }
    if (this._permission_match(permissions, permission)) {
      return true;
    }
    if (this._permission_match(permissions,
      this._all_resource_permission(permission))) {
      return true;
    }
    if (this._permission_match(permissions, ADMIN_PERMISSION)) {
      return true;
    }
    if (this._permission_match(permissions,
      this._admin_permission_for_context(permission.context_id))) {
      return true;
    }
    // Check for System Admin permission
    if (this._permission_match(permissions,
      this._admin_permission_for_context(0))) {
      return true;
    }
    return false;
  },

  _resolve_permission_variable: function (value) {
    if ($.type(value) === 'string') {
      if (value[0] === '$') {
        if (value === '$current_user') {
          return getInstance('Person', GGRC.current_user.id);
        }
        throw new Error('unknown permission variable: ' + value);
      }
    }
    return value;
  },

  is_allowed: function (action, resourceType, contextId) {
    return this._is_allowed(
      permissionsCompute(), new this(action, resourceType, contextId));
  },

  is_allowed_for: function (action, resource) {
    return !!resource.actions[action]
  },

  is_allowed_any: function (action, resourceType) {
    let allowed = this.is_allowed(action, resourceType);
    let perms = permissionsCompute();

    if (!allowed) {
      allowed = _.exists(perms, action, resourceType, 'contexts', 'length');
    }
    return !!allowed;
  },

  page_context_id: function () {
    let pageInstance = getPageInstance();
    return (pageInstance && pageInstance.context &&
            pageInstance.context.id) || null;
  },

  refresh: function () {
    return $.ajax({
      url: '/permissions',
      type: 'get',
      dataType: 'json',
    }).then(function (perm) {
      permissionsCompute(perm);
      GGRC.permissions = perm;
    });
  },
}, {
  // prototype
  setup: function (action, resourceType, contextId) {
    this.action = action;
    this.resource_type = resourceType;
    this.context_id = contextId;
    return this;
  },
});

ADMIN_PERMISSION = new Permission('__GGRC_ADMIN__', '__GGRC_ALL__', 0);

export default Permission;
