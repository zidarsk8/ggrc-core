/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import {warning} from './modals';

/**
 * Utils methods shared between GGRC controllers (GGRC.Controllers)
 */
let typesWithWarning = ['System', 'Process', 'Product'];

function checkPreconditions(options, success) {
  let instance = options.instance;
  let operation = options.operation;
  let conditions = options.extraConditions || [];

  if (!hasWarningType(instance)) {
    success();
    return;
  }

  if (!_checkExtraConditions(conditions)) {
    success();
    return;
  }

  warning({
    objectShortInfo: [instance.type, instance.title].join(' '),
    operation: operation
  }, success);
}

function becameDeprecated(instance, prevStatus) {
  let status = instance && instance.status;

  return (
    !_.isEqual(status, prevStatus) && // status was changed
    _.isEqual(status, 'Deprecated')
  );
}

function hasWarningType(instance) {
  return (
    instance &&
    _.includes(typesWithWarning, instance.type)
  );
}

function _checkExtraConditions(conditions) {
  return _.every(conditions, function (condition) {
    return condition();
  });
}

function shouldApplyPreconditions(instance) {
  return hasWarningType(instance);
}

export {
  checkPreconditions,
  hasWarningType,
  becameDeprecated,
  shouldApplyPreconditions,
};
