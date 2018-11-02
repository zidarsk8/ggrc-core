/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

export default can.Construct({
  defaults: {
    whileQueueHasElements: function () {},
    whenQueueEmpties: function () {},
  },
}, {
  init: function (options) {
    this.dfds = [];
    this.onEmptyCallbacksList = [];

    can.each(this.constructor.defaults, (val, key) => {
      this[key] = val;
    });
    can.each(options, (val, key) => {
      this[key] = val;
    });
  },
  queue: function (dfd) {
    let that = this;
    if (!dfd || !dfd.then) {
      throw new Error('Attempted to queue something other than a ' +
                      'Deferred or Promise');
    }

    if (!_.includes(this.dfds, dfd)) {
      this.dfds.push(dfd);
      dfd.always(function () {
        let dfdIndex = that.dfds.indexOf(dfd);
        if (dfdIndex > -1) {
          that.dfds.splice(dfdIndex, 1);
        }

        if (that.dfds.length === 0) {
          can.each(that.onEmptyCallbacksList, Function.prototype.call);
          that.onEmptyCallbacksList = [];
          that.whenQueueEmpties();
        }
      });
    }

    let pendingCallbacks = this.onEmptyCallbacksList.length;
    if (pendingCallbacks === 0 && that.dfds.length > 0) {
      that.whileQueueHasElements();
    }
  },
  onEmpty: function (fn) {
    if (this.dfds.length === 0) {
      fn();
    }
    if (this.dfds.length > 0 && !this.onEmptyCallbacksList.includes(fn)) {
      this.onEmptyCallbacksList.push(fn);
    }
  },
});
