/*
    Copyright (C) 2018 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

export default can.extend(can.Control.prototype, {
  // Returns a function which will be halted unless `this.element` exists
  //   - useful for callbacks which depend on the controller's presence in
  //     the DOM
  _ifNotRemoved(fn) {
    let that = this;
    return function () {
      if (!that.element) {
        return;
      }
      return fn.apply(this, arguments);
    };
  },
});
