/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import Mixin from './mixin';

export default Mixin.extend({
  'after:init'() {
    if (GGRC.GGRC_Q_INTEGRATION_URL) {
      this.tree_view_options.attr_list.push({
        attr_title: 'Questionnaire',
        attr_name: 'questionnaire',
        disable_sorting: true,
      });
      this.isQuestionnaireable = true;
    }
  },
}, {});
