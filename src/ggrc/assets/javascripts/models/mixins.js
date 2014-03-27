/*!
    Copyright (C) 2014 Google Inc., authors, and contributors <see AUTHORS file>
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
    Created By: brad@reciprocitylabs.com
    Maintained By: brad@reciprocitylabs.com
*/

;(function(can) {

can.Construct("can.Model.Mixin", {
  extend: function(fullName, klass, proto) {
    var tempname, parts, shortName;
    if(typeof fullName === "string") {
      // Mixins do not go into the global namespace.
      tempname = fullName;
      fullName = null;
    }
    var Constructor = this._super.call(this, fullName, klass, proto);

    //instead mixins sit under CMS.Models.Mixins
    if(tempname) {
      parts = tempname.split(".");
      shortName = parts.pop();
      Constructor.fullName = tempname;
    } else {
      Constructor.fullName = shortName = "Mixin_" + Math.floor(Math.random() * Math.pow(36, 8)).toString(36);
      parts = [];
    }
      can.getObject("CMS.Models.Mixins"
                    + (parts.length ? "." + parts.join(".") : "")
                    , window
                    , true)[shortName] = Constructor;
    return Constructor;
  }
  , newInstance : function() {
    throw "Mixins cannot be directly instantiated";
  }
  , add_to : function(cls) {
    if(this === can.Model.Mixin) {
      throw "Must only add a subclass of Mixin to an object, not Mixin itself";
    }
    var setupfns = function(obj) {
      return function(fn, key) {
        var blockedKeys = ["fullName", "defaults", "_super", "constructor"];
        if(fn !== can.Model.Mixin[key] && !~can.inArray(key, blockedKeys)) {
          var oldfn = obj[key];
          // TODO support other ways of adding functions.
          //  E.g. "override" (doesn't call super fn at all) 
          //       "sub" (sets this._super for mixin function)
          //       "chain" (pushes result of oldfn onto args)
          //       "before"/"after" (overridden function)
          // TODO support extension for objects.  
          //   Necessary for "attributes"/"serialize"/"convert"
          // Defaults will always be "after" for functions
          //  and "override" for non-function values
          if(oldfn && typeof oldfn === "function") {
            obj[key] = function() {
              oldfn.apply(this, arguments);
              return fn.apply(this, arguments);
            };
          } else {
            obj[key] = fn;
          }
        }
      };
    };

    if(!~can.inArray(this.fullName, cls._mixins)) {
      cls._mixins = cls._mixins || [];
      cls._mixins.push(this.fullName);

      can.each(this, setupfns(cls));
      can.each(this.prototype, setupfns(cls.prototype));
    }
  }
}, {
});

can.Model.Mixin("ownable", {
  before_create : function() {
    if(!this.owners || this.owners.length === 0) {
      this.attr('owners', [{ id: GGRC.current_user.id }]);
    }
  }
});

can.Model.Mixin("contactable" ,{
  before_create : function() {
    if(!this.contact) {
      this.attr('contact', { id: GGRC.current_user.id, type : "Person" });
    }
  }
});

can.Model.Mixin("assignable", {
  before_create : function() {
    if(!this.assignee) {
      this.attr('assignee', { id: GGRC.current_user.id, type : "Person" });
    }
  }
});


})(this.can);
