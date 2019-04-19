/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

export default can.Model.extend({
  root_object: 'saved_search',
  root_collection: 'saved_searches',
  findOne: 'GET /api/saved_searches/{id}',
  findAll: 'GET /api/saved_searches',
  update: 'PUT /api/saved_searches/{id}',
  destroy: 'DELETE /api/saved_searches/{id}',
  create: 'POST /api/saved_searches',
  init: function () {
    this.validatePresenceOf('name');
    this.validatePresenceOf('query');
    this.validatePresenceOf('object_type');
    if (this._super) {
      this._super(...arguments);
    }
  },
}, {});

