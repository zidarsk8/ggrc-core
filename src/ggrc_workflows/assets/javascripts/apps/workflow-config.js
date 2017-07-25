/*
 * Copyright (C) 2017 Google Inc.
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC) {
  GGRC.Workflow = {
    unitOptions: [
      {title: 'Daily', value: 'day', plural: 'days', singular: 'day'},
      {title: 'Weekly', value: 'week', plural: 'weeks', singular: 'week'},
      {title: 'Monthly', value: 'month', plural: 'months', singular: 'month'}
    ],
    repeatOptions: _.range(1, 31)
      .map(function (option) {
        return {
          value: option
        };
      }),
    defaultRepeatValues: {
      unit: 'month',
      repeatEvery: 1
    }
  };
})(window.GGRC);
