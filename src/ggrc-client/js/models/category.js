/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

can.Model.Cacheable('CMS.Models.CategoryBase', {
  root_object: 'category_base',
  root_collection: 'category_bases',
  root_model: 'CategoryBase',
  findAll: 'GET /api/category_bases',
  findOne: 'GET /api/category_bases/{id}',
  attributes: {
    children: 'CMS.Models.Category.stubs',
    owners: 'CMS.Models.Person.stubs',
  },
  tree_view_options: {
    show_view: '/static/mustache/controls/categories_tree.mustache',
    start_expanded: false,
  },
}, {
});

CMS.Models.CategoryBase('CMS.Models.ControlCategory', {
  root_object: 'control_category',
  root_collection: 'control_categories',
  findAll: 'GET /api/control_categories',
  findOne: 'GET /api/control_categories/{id}',
}, {
});

CMS.Models.CategoryBase('CMS.Models.ControlAssertion', {
  root_object: 'control_assertion',
  root_collection: 'control_assertions',
  findAll: 'GET /api/control_assertions',
  findOne: 'GET /api/control_assertions/{id}',
}, {
});
