/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
import {notifierXHR} from '../../plugins/utils/notifiers-utils';

export default CanComponent.extend({
  tag: 'inline-form-control',
  leakScope: true,
  viewModel: CanMap.extend({
    deferredSave: null,
    instance: null,

    saveInlineForm: function (args) {
      let self = this;

      this.attr('deferredSave').push(function () {
        self.attr('instance.' + args.propName, args.value);
      }).fail(function (instance, xhr) {
        notifierXHR('error', xhr);
      });
    },
  }),
});
