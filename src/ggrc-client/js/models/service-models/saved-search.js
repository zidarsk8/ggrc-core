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
  findBy(objectType, searchType, paging) {
    let url = `/api/saved_searches/${objectType}?search_type=${searchType}`;

    if (paging) {
      const offset = (paging.current - 1) * paging.pageSize;
      const limit = paging.pageSize;
      url += `&offset=${offset}&limit=${limit}`;
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
