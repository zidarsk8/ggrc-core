/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can) {
  'use strict';

  /**
   * The util allows to perform batch of actions with some delay in a single transaction.
   * @param {function} completeTransaction - The function that allows to submit result of transaction.
   * @param {number} timeout - The execution delay in milliseconds.
   */
  GGRC.Utils.DeferredTransaction = function (completeTransaction, timeout) {
    var deferredQueue = [];
    var timeoutId = null;

    function runQueue(queue) {
      can.each(queue, function (actionItem) {
        actionItem.action();
      });
    }

    function resolveQueue(queue, result) {
      can.each(queue, function (actionItem) {
        actionItem.deferred.resolve(result);
      });
    }

    function rejectQueue(queue, result) {
      can.each(queue, function (actionItem) {
        actionItem.deferred.reject(result);
      });
    }

    /**
     * Adds new action to execution queue.
     * @param {function} action - The action that should be executed.
     * @return {object} - The canJS promise indicates result of the transaction.
     */
    this.push = function (action) {
      var dfd = can.Deferred();
      deferredQueue.push({
        deferred: dfd,
        action: action
      });

      if (timeoutId) {
        clearTimeout(timeoutId);
      }

      timeoutId = setTimeout(function () {
        var currentQueue = deferredQueue.slice();
        runQueue(currentQueue);

        completeTransaction(
          resolveQueue.bind(this, currentQueue),
          rejectQueue.bind(this, currentQueue));

        deferredQueue = deferredQueue.filter(function (action) {
          return currentQueue.indexOf(action) < 0;
        });
      }, timeout);

      return dfd.promise();
    };
  };
})(window.can);
