/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Cacheable from '../cacheable';
import uniqueTitle from '../mixins/unique-title';
import timeboxed from '../mixins/timeboxed';
import caUpdate from '../mixins/ca-update';
import baseNotifications from '../mixins/base-notifications';
import Stub from '../stub';

export default Cacheable('CMS.Models.Directive', {
  root_object: 'directive',
  root_collection: 'directives',
  category: 'governance',
  // `rootModel` overrides `model.shortName` when determining polymorphic types
  root_model: 'Directive',
  findAll: '/api/directives',
  findOne: '/api/directives/{id}',
  mixins: [uniqueTitle, timeboxed, caUpdate, baseNotifications],
  tree_view_options: {
    attr_view: GGRC.mustache_path + '/directives/tree-item-attr.mustache',
    attr_list: Cacheable.attr_list.concat([
      {attr_title: 'Reference URL', attr_name: 'reference_url'},
      {attr_title: 'Effective Date', attr_name: 'start_date'},
      {attr_title: 'Last Deprecated Date', attr_name: 'end_date'},
      {
        attr_title: 'State',
        attr_name: 'status',
        order: 40,
      }, {
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
      }, {
        attr_title: 'Review State',
        attr_name: 'review_status',
        order: 80,
      }]),
    add_item_view: GGRC.mustache_path + '/snapshots/tree_add_item.mustache',
  },
  attributes: {
    context: Stub,
    modified_by: Stub,
  },
  init: function () {
    this.validateNonBlank('title');
    this._super(...arguments);
  },
}, {});
