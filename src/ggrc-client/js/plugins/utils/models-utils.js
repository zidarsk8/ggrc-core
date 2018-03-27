/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import RefreshQueue from '../../models/refresh_queue';

const relatedAssessmentsTypes = Object.freeze(['Control', 'Objective']);

const getModelInstance = (id, type, requiredAttr) => {
  const promise = new Promise((resolve, reject) => {
    let modelInstance;

    if (!id || !type || !requiredAttr) {
      reject();
    }

    modelInstance = CMS.Models[type].findInCacheById(id) || {};

    if (modelInstance && modelInstance.hasOwnProperty(requiredAttr)) {
      resolve(modelInstance);
    } else {
      modelInstance = new CMS.Models[type]({id: id});
      new RefreshQueue()
        .enqueue(modelInstance)
        .trigger()
        .done((data) => {
          data = Array.isArray(data) ? data[0] : data;
          resolve(data);
        })
        .fail(function () {
          GGRC.Errors
            .notifier('error', `Failed to fetch data for ${type}: ${id}.`);
          reject();
        });
    }
  });

  return promise;
};

/**
 * Check the model has Related Assessments
 * @param {String} type - model type
 * @return {Boolean}
 */
const hasRelatedAssessments = (type) => {
  return _.contains(relatedAssessmentsTypes, type);
};

export {
  getModelInstance,
  hasRelatedAssessments,
  relatedAssessmentsTypes,
};
