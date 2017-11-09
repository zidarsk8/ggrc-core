/*
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

/**
 *
 * @event refreshRelated
 * @type {object}
 * @property {string} type - Event name.
 * @property {string} model -  Model name.
 */
const REFRESH_RELATED = {
  type: 'refreshRelated',
};

/**
 *
 * @event saveCustomRole
 * @type {object}
 * @property {string} type - Event name.
 * @property {string} groupId - Role ID.
 */
const SAVE_CUSTOM_ROLE = {
  type: 'saveCustomRole',
};

/**
 *
 * @event rolesConflict
 * @type {object}
 * @property {string} type - Event name.
 * @property {string} groupId - Role ID.
 */
const ROLES_CONFLICT = {
  type: 'rolesConflict',
};

export {
  REFRESH_RELATED,
  SAVE_CUSTOM_ROLE,
  ROLES_CONFLICT,
};
