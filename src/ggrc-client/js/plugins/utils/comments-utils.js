/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import * as QueryAPI from './query-api-utils';

async function loadComments(relevantObject, modelName,
  startIndex = 0, count = 10) {
  let query = buildQuery(relevantObject, modelName, startIndex, count);

  return QueryAPI.batchRequests(query);
}

function buildQuery(relevantObject, modelName, startIndex, count) {
  return QueryAPI.buildParam(modelName, {
    first: startIndex,
    last: startIndex + count,
    sort: [{
      key: 'created_at',
      direction: 'desc',
    }]}, {
    type: relevantObject.type,
    id: relevantObject.id,
    operation: 'relevant',
  });
}

export {
  loadComments,
};
