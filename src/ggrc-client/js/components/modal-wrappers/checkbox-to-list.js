/*
    Copyright (C) 2019 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import CanMap from 'can-map';
import CanComponent from 'can-component';
export default CanComponent.extend({
  tag: 'checkbox-to-list',
  leakScope: true,
  viewModel: CanMap.extend({
    property: '',
    instance: null,
    values: {},
  }),
  init: function () {
    let viewModel = this.viewModel;
    let values = viewModel.attr('instance.' + viewModel.attr('property'));

    if (values && _.isString(values)) {
      _.forEach(_.splitTrim(values, ','), function (val) {
        if (val) {
          viewModel.attr('values.' + val, true);
        }
      });
    }
  },
  events: {
    '{viewModel.values} change': function () {
      let viewModel = this.viewModel;
      let values = _.keys(
        _.pickBy(
          viewModel.attr('values').serialize(),
          _.identity
        )
      );
      viewModel.instance.attr(viewModel.attr('property'), values.join(','));
    },
  },
});
