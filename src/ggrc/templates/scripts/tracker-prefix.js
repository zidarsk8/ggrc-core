/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

GGRC.Tracker = {
  _pending_emit : []
  , timing: function(a,b,c,d) {
    this._pending_emit.push({
      hitType: 'timing'
      , timingCategory : a
      , timingVar : b
      , timingValue : +c
      , timingLabel : d
    });
  }
  , start : function(a,b,c) {
    var d = Date.now(), t = this;
    return function() {
      t.timing(a,b, Date.now() - d, c);
    };
  }
};
