/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

export default class PersistentNotifier {
  constructor(options) {
    this.dfds = [];
    this.onEmptyCallbacksList = [];

    Object.assign(this, options);
  }

  whileQueueHasElements() {}

  whenQueueEmpties() {}

  queue(dfd) {
    if (!dfd || !dfd.then) {
      throw new Error('Attempted to queue something other than a ' +
                      'Deferred or Promise');
    }

    if (!this.dfds.includes(dfd)) {
      this.dfds.push(dfd);
      dfd.always(function () {
        let dfdIndex = this.dfds.indexOf(dfd);
        if (dfdIndex > -1) {
          this.dfds.splice(dfdIndex, 1);
        }

        if (this.dfds.length === 0) {
          this.onEmptyCallbacksList.forEach(Function.prototype.call);
          this.onEmptyCallbacksList = [];
          this.whenQueueEmpties();
        }
      });
    }

    let pendingCallbacks = this.onEmptyCallbacksList.length;
    if (pendingCallbacks === 0 && this.dfds.length > 0) {
      this.whileQueueHasElements();
    }
  }

  onEmpty(fn) {
    if (this.dfds.length === 0) {
      fn();
    }
    if (this.dfds.length > 0 && !this.onEmptyCallbacksList.includes(fn)) {
      this.onEmptyCallbacksList.push(fn);
    }
  }
}
