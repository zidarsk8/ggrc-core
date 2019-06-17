/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

export default can.Model.extend({
  root_object: 'saved_search',
  root_collection: 'saved_searches',
  update: 'PUT /api/saved_searches/{id}',
  destroy: 'DELETE /api/saved_searches/{id}',
  create: 'POST /api/saved_searches',
  findOne: 'GET /api/saved_searches/{id}',
  ajax: $.ajax,
  findBy(searchType, paging, objectType) {
    let url = `/api/saved_searches/${searchType}`;

    if (paging) {
      const offset = (paging.current - 1) * paging.pageSize;
      url += `?offset=${offset}&limit=${paging.pageSize}`;
    }

    if (objectType) {
      url += `${paging ? '&' : '?'}object_type=${objectType}`;
    }

    return $.ajax({
      url,
      type: 'get',
      dataType: 'json',
    });
  },
}, {
  define: {
    name: {
      value: '',
      validate: {
        required: true,
      },
    },
    object_type: {
      value: '',
      validate: {
        required: true,
      },
    },
  },
});
