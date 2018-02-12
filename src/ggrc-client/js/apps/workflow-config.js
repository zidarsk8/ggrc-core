/*
 * Copyright (C) 2018 Google Inc.
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC) {
  GGRC.Workflow = {
    unitOptions: [
      {title: 'Weekday', value: 'day', plural: 'weekdays', singular: 'weekday'},
      {title: 'Weekly', value: 'week', plural: 'weeks', singular: 'week'},
      {title: 'Monthly', value: 'month', plural: 'months', singular: 'month'},
    ],
    repeatOptions: _.range(1, 31)
      .map(function (option) {
        return {
          value: option,
        };
      }),
    defaultRepeatValues: {
      unit: 'month',
      repeatEvery: 1,
    },
  };
})(window.GGRC);
