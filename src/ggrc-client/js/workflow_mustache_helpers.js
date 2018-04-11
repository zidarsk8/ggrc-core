/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

/*
  if_recurring_workflow mustache helper

  Given an object, it  determines if it's a workflow, and if it's a recurring
  workflow or not.

  @param object - the object we want to check
  */
Mustache.registerHelper('if_recurring_workflow', function (object, options) {
  object = Mustache.resolve(object);
  if (object.type === 'Workflow' &&
      _.includes(['day', 'week', 'month'], object.unit)) {
    return options.fn(this);
  }
  return options.inverse(this);
});
