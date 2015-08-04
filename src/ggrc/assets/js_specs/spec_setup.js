/*!
 Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 Created By: swizec@reciprocitylabs.com
 Maintained By: anze@reciprocitylabs.com
 */

/*

Spec setup file.
*/

window.GGRC = window.GGRC || {};
GGRC.current_user = GGRC.current_user || { id : 1, type : "Person" };
GGRC.permissions = {
  create: {},
  delete: {},
  read: {},
  update: {},
  view_object_page: {},
};
GGRC.config = {};
