/*
 * Copyright (C) 2017 Google Inc.
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC) {
  GGRC.Workflow = {
    unitOptions: [
      {title: 'Daily', value: 'Day', plural: 'days', singular: 'day'},
      {title: 'Weekly', value: 'Week', plural: 'weeks', singular: 'week'},
      {title: 'Monthly', value: 'Month', plural: 'months', singular: 'month'}
    ],
    repeatOptions: _.range(1, 31)
      .map(function (option) {
        return {
          value: option
        };
      }),
    defaultRepeatValues: {
      unit: 'Month',
      repeatEvery: 1
    }
  };
})(window.GGRC);
