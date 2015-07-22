/*
 * Copyright (C) 2015 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By: ivan@reciprocitylabs.com
 * Maintained By: ivan@reciprocitylabs.com
 */

Mustache.registerHelper("if_equals", function(val1, val2, options) {
  var that = this, _val1, _val2;
  function exec() {
    if(_val1 == _val2) return options.fn(options.contexts);
    else return options.inverse(options.contexts);
  }
    if(typeof val1 === "function") {
      if(val1.isComputed) {
        val1.bind("change", function(ev, newVal, oldVal) {
          _val1 = newVal;
          return exec();
        });
      }
      _val1 = val1.call(this);
    } else {
      _val1 = val1;
    }
    if(typeof val2 === "function") {
      if(val2.isComputed) {
        val2.bind("change", function(ev, newVal, oldVal) {
          _val2 = newVal;
          exec();
        });
      }
      _val2 = val2.call(this);
    } else {
      _val2 = val2;
    }

  return exec();
});
Mustache.registerHelper("if_grater", function(val1, val2, options) {
  var that = this, _val1, _val2;
  function exec() {
    if(_val1 > _val2) return options.fn(options.contexts);
    else return options.inverse(options.contexts);
  }
    if(typeof val1 === "function") {
      if(val1.isComputed) {
        val1.bind("change", function(ev, newVal, oldVal) {
          _val1 = newVal;
          return exec();
        });
      }
      _val1 = val1.call(this);
    } else {
      _val1 = val1;
    }
    if(typeof val2 === "function") {
      if(val2.isComputed) {
        val2.bind("change", function(ev, newVal, oldVal) {
          _val2 = newVal;
          exec();
        });
      }
      _val2 = val2.call(this);
    } else {
      _val2 = val2;
    }

  return exec();
});

Mustache.registerHelper("is_overdue", function(val1, options) {
  var that = this, _val1;
  function exec() {
    if(+new Date() > +new Date(_val1)) return options.fn(options.contexts);
    else return options.inverse(options.contexts);
  }
    if(typeof val1 === "function") {
      if(val1.isComputed) {
        val1.bind("change", function(ev, newVal, oldVal) {
          _val1 = newVal;
          return exec();
        });
      }
      _val1 = val1.call(this);
    } else {
      _val1 = val1;
    }

  return exec();
});
