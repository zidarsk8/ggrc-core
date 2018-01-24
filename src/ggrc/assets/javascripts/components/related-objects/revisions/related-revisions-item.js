/*
 Copyright (C) 2018 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {
  getInstanceView,
} from '../../../plugins/utils/object-history-utils';

import '../../diff/instance-fields-diff';
import '../../diff/instance-acl-diff';
import '../../diff/instance-gca-diff';
import '../../diff/instance-mapping-fields-diff';
import '../../diff/instance-list-fields-diff';
import '../../revision-history/restored-revision-comparer-config';
import template from './templates/related-revisions-item.mustache';
const tag = 'related-revisions-item';

export default can.Component.extend({
  tag,
  template,
  viewModel: {
    define: {
      instance: {
        set(newValue, setValue) {
          if (!newValue) {
            return;
          }

          // revision-comparer expects view path
          newValue.attr('view', getInstanceView(newValue));
          setValue(newValue);
        },
      },
      revision: {
        set(newValue, setValue) {
          if (!newValue) {
            return;
          }

          GGRC.Utils.getPersonInfo(newValue.modified_by).then((person) => {
            this.attr('modifiedBy', person);
          });

          setValue(newValue);
        },
      },
      isCreated: {
        get() {
          return this.attr('revision.action') === 'created';
        },
      },
    },
    modifiedBy: {},
    lastRevision: {},
  },
});
