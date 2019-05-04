/*
  Copyright (C) 2019 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import DeferredTransaction from '../../utils/deferred-transaction-utils';

describe('DeferredTransaction module', function () {
  let deferredTransaction;
  let completeTransactionCount;
  let completeActionsCount;

  function action() {
    completeActionsCount++;
  }

  beforeAll(function () {
    deferredTransaction = new DeferredTransaction(
      function (resolve, reject) {
        completeTransactionCount++;
        resolve();
      }, 100);
  });

  beforeEach(function () {
    completeTransactionCount = 0;
    completeActionsCount = 0;
  });

  it('make several sequence transactions when actions ' +
    'were added with delay greater than configured', function (done) {
    deferredTransaction.push(action).then(function () {
      completeTransactionCount = 0;
    });
    setTimeout(function () {
      deferredTransaction.push(action).then(function () {
        expect(completeTransactionCount).toBe(1);
        expect(completeActionsCount).toBe(2);
        done();
      });
    }, 150);
  });

  it('make one transaction when actions were added with delay ' +
    'less than configured', function (done) {
    deferredTransaction.push(action);
    setTimeout(function () {
      deferredTransaction.push(action).then(function () {
        expect(completeTransactionCount).toBe(1);
        expect(completeActionsCount).toBe(2);
        done();
      });
    }, 50);
  });

  it('execute queue of actions with 0 timeout if "execute" method was called',
    (done) => {
      deferredTransaction.push(action);
      deferredTransaction.execute(action);
      setTimeout(() => {
        expect(completeTransactionCount).toBe(1);
        expect(completeActionsCount).toBe(2);
        done();
      }, 10);
    });
});
