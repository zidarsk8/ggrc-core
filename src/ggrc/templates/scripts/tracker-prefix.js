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
