/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import SystemOrProcess from './system-or-process';
import {hasQuestions} from '../../plugins/utils/ggrcq-utils';

export default SystemOrProcess('CMS.Models.Process', {
  root_object: 'process',
  root_collection: 'processes',
  model_plural: 'Processes',
  table_plural: 'processes',
  title_plural: 'Processes',
  model_singular: 'Process',
  title_singular: 'Process',
  table_singular: 'process',
  findAll: 'GET /api/processes',
  findOne: 'GET /api/processes/{id}',
  create: 'POST /api/processes',
  update: 'PUT /api/processes/{id}',
  destroy: 'DELETE /api/processes/{id}',
  cache: can.getObject('cache', CMS.Models.SystemOrProcess, true),
  is_custom_attributable: true,
  isRoleable: true,
  attributes: {},
  defaults: {
    title: '',
    url: '',
    status: 'Draft',
  },
  sub_tree_view_options: {
    default_filter: ['Risk'],
  },
  statuses: ['Draft', 'Deprecated', 'Active'],
  init: function () {
    can.extend(this.attributes, CMS.Models.SystemOrProcess.attributes);
    this._super && this._super(...arguments);
    this.tree_view_options = $.extend(true, {},
      CMS.Models.SystemOrProcess.tree_view_options);

    if (hasQuestions(this.shortName)) {
      this.tree_view_options.attr_list.push({
        attr_title: 'Questionnaire',
        attr_name: 'questionnaire',
        disable_sorting: true,
      });
    }
    this.validateNonBlank('title');
  },
}, {
  init: function () {
    this._super && this._super(...arguments);
    this.attr('is_biz_process', true);
  },
});
