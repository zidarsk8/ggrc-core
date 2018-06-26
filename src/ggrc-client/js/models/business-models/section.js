/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

export default can.Model.Cacheable('CMS.Models.Section', {
  root_object: 'section',
  root_collection: 'sections',
  model_plural: 'Sections',
  table_plural: 'sections',
  title_plural: 'Sections',
  model_singular: 'Section',
  title_singular: 'Section',
  table_singular: 'section',
  category: 'governance',
  root_model: 'Section',
  findAll: 'GET /api/sections',
  findOne: 'GET /api/sections/{id}',
  create: 'POST /api/sections',
  update: 'PUT /api/sections/{id}',
  destroy: 'DELETE /api/sections/{id}',
  is_custom_attributable: true,
  isRoleable: true,
  mixins: [
    'unique_title',
    'ca_update',
    'accessControlList',
    'base-notifications',
  ],
  attributes: {
    context: 'CMS.Models.Context.stub',
    modified_by: 'CMS.Models.Person.stub',
    object_people: 'CMS.Models.ObjectPerson.stubs',
    people: 'CMS.Models.Person.stubs',
    directive: 'CMS.Models.get_stub',
    children: 'CMS.Models.get_stubs',
    directive_sections: 'CMS.Models.DirectiveSection.stubs',
    directives: 'CMS.Models.get_stubs',
    objectives: 'CMS.Models.Objective.stubs',
  },
  tree_view_options: {
    attr_view: '/static/mustache/sections/tree-item-attr.mustache',
    attr_list: can.Model.Cacheable.attr_list.concat([
      {attr_title: 'Reference URL', attr_name: 'reference_url'},
      {attr_title: 'Effective Date', attr_name: 'start_date'},
      {attr_title: 'Last Deprecated Date', attr_name: 'last_deprecated_date'},
      {
        attr_title: 'Description',
        attr_name: 'description',
        disable_sorting: true,
      }, {
        attr_title: 'Notes',
        attr_name: 'notes',
        disable_sorting: true,
      }, {
        attr_title: 'Assessment Procedure',
        attr_name: 'test_plan',
        disable_sorting: true,
      }]),
    add_item_view: GGRC.mustache_path + '/snapshots/tree_add_item.mustache',
  },
  sub_tree_view_options: {
    default_filter: ['Objective'],
  },
  defaults: {
    status: 'Draft',
  },
  statuses: ['Draft', 'Deprecated', 'Active'],
  init: function () {
    this._super(...arguments);
    this.validateNonBlank('title');
  },
}, {});
