/*
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

/**
 * Adjust date to the closest week day that is less than current.
 *
 * @param {Date} date - date value
 *
 * @return {Date} closest week date to provided
 */
function getClosestWeekday(date) {
  let momDate = moment(date);

  if (momDate.isoWeekday() > 5) {
    return momDate.isoWeekday(5).toDate();
  }

  return date;
};

export {
  getClosestWeekday,
};
