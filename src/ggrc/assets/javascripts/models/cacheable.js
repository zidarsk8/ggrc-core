/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all

(function(can) {

var makeFindRelated = function(thistype, othertype) {
  return function(params) {
    if(!params[thistype + "_type"]) {
      params[thistype + "_type"] = this.shortName;
    }
    return CMS.Models.Relationship.findAll(params).then(function(relationships) {
      var dfds = [], things = new can.Model.List();
      can.each(relationships, function(rel,idx) {
        var dfd;
        if(rel[othertype].selfLink) {
          things.push(rel[othertype]);
        } else {
          dfd = rel[othertype].refresh().then(function(dest) {
            things.splice(idx, 1, dest);
          });
          dfds.push(dfd);
          things.push(dfd);
        }
      });
      return $.when.apply($, dfds).then(function(){ return things; });
    });
  };
};


can.Model("can.Model.Cacheable", {

  findOne : "GET {href}"
  , setup : function(construct, name, statics, prototypes) {
    if((!statics || !statics.findAll) && this.findAll === can.Model.Cacheable.findAll)
      this.findAll = "GET /api/" + this.root_collection;

    if(this.root_collection) {
      this.model_plural = statics.model_plural || this.root_collection.replace(/(?:^|_)([a-z])/g, function(s, l) { return l.toUpperCase(); } );
      this.title_plural = statics.title_plural || this.root_collection.replace(/(^|_)([a-z])/g, function(s, u, l) { return (u ? " " : "") + l.toUpperCase(); } );
      this.table_plural = statics.table_plural || this.root_collection;
    }
    if(this.root_object) {
      this.model_singular = statics.model_singular || this.root_object.replace(/(?:^|_)([a-z])/g, function(s, l) { return l.toUpperCase(); } );
      this.title_singular = statics.title_singular || this.root_object.replace(/(^|_)([a-z])/g, function(s, u, l) { return (u ? " " : "") + l.toUpperCase(); } );
      this.table_singular = statics.table_singular || this.root_object;
    }

    return this._super.apply(this, arguments);
  }
  , init : function() {
    this.bind("created", function(ev, new_obj) {
      var cache = can.getObject("cache", new_obj.constructor, true);
      if(new_obj.id) {
        cache[new_obj.id] = new_obj;
        if(cache[undefined] === new_obj)
          delete cache[undefined];
      }
    });
    this.bind("destroyed", function(ev, old_obj) {
      delete can.getObject("cache", old_obj.constructor, true)[old_obj.id];
    });
    //can.getObject("cache", this, true);

    var _update = this.update;
    this.update = function(id, params) {
      var ret = _update
        .call(this, id, this.process_args(params))
        .fail(function(status) {
          if(status === 409) {
            //handle conflict.
          }
        });
      delete ret.hasFailCallback;
      return ret;
    };

    var _create = this.create;
    this.create = function(params) {
      var ret = _create
        .call(this, this.process_args(params));
      delete ret.hasFailCallback;
      return ret;
    };


    var _refresh = this.makeFindOne({ type : "get", url : "{href}" });
    this.refresh = function(params) {
      return _refresh.call(this, {href : params.selfLink || params.href});
    };

    var that = this;
    this.risk_tree_options = can.extend(true, {}, this.risk_tree_options); //for subclasses
    var risk_child_options = that.risk_tree_options.child_options[0];
    this.risk_tree_options.list_view = GGRC.mustache_path + "/base_objects/tree.mustache";
    if(risk_child_options) {
      risk_child_options.find_params.destination_type = that.shortName;
      risk_child_options.find_params.relationship_type_id = "risk_is_a_threat_to_" + this.root_object;
    }
    $(function() {
      if(risk_child_options)
        risk_child_options.model = CMS.Models.Risk;
      if(that.risk_tree_options.child_options && that.risk_tree_options.child_options.length > 1)
        that.risk_tree_options.child_options[1].model = that;
    });


  }

  , findInCacheById : function(id) {
    return can.getObject("cache", this, true)[id];
  }

  , newInstance : function(args) {
    var cache = can.getObject("cache", this, true);
    if(args && args.id && cache[args.id]) {
      //cache[args.id].attr(args, false); //CanJS has bugs in recursive merging 
                                          // (merging -- adding properties from an object without removing existing ones 
                                          //  -- doesn't work in nested objects).  So we're just going to not merge properties.
      return cache[args.id];
    } else {
      return can.Model.Cacheable.prototype.__proto__.constructor.newInstance.apply(this, arguments);
    }
  }
  , process_args : function(args, names) {
    var pargs = {};
    var obj = pargs;
    if(this.root_object && !(this.root_object in args)) {
      obj = pargs[this.root_object] = {};
    }
    var src = args.serialize ? args.serialize() : args;
    var go_names = (!names || names.not) ? Object.keys(src) : names;
    for(var i = 0 ; i < (go_names.length || 0) ; i++) {
      obj[go_names[i]] = src[go_names[i]];
    }
    if(names && names.not) {
      var not_names = names.not;
      for(i = 0 ; i < (not_names.length || 0) ; i++) {
        delete obj[not_names[i]];
      }
    }
    return pargs;
  }
  , findRelated : makeFindRelated("source", "destination")
  , findRelatedSource : makeFindRelated("destination", "source")
  , models : function(params) {
    if(params[this.root_collection + "_collection"]) {
      params = params[this.root_collection + "_collection"];
    }
    if(params[this.root_collection]) {
      params = params[this.root_collection];
    }
    var ms = this._super(params);
    if(params instanceof can.Observe) {
      params.replace(ms);
      return params;
    } else {
      return ms;
    }
  }
  , model : function(params) {
    var m, that = this;
    var obj_name = this.root_object;
    if(typeof obj_name !== "undefined" && params[obj_name]) {
        for(var i in params[obj_name]) {
          if(params[obj_name].hasOwnProperty(i)) {
            params.attr
            ? params.attr(i, params[obj_name][i])
            : (params[i] = params[obj_name][i]);
          }
        }
        if(params.removeAttr) {
          params.removeAttr(obj_name);
        } else {
          delete params[obj_name];
        }
    }
    if(m = this.findInCacheById(params.id)) {
      if(!m.selfLink) {
        //we are fleshing out a stub, which is much like creating an object new.
        //But we don't want to trigger every change event on the new object's props.
        m._init = 1;
      }
      var fn = (typeof params.each === "function") ? can.proxy(params.each,"call") : can.each;
      fn(params, function(val, key) {
        var p = val && val.serialize ? val.serialize() : val;
        if(m[key] instanceof can.Observe.List) {
          m[key].replace(
            m[key].constructor.models ?
              m[key].constructor.models(p)
              : p);
        } else if(m[key] instanceof can.Model) {
          m[key].constructor.model(params[key]);
        } else {
          m.attr(key, p);
        }
      });
      delete m._init;
    } else {
      m = this._super(params);
    }
    return m;
  }
  , tree_view_options : {}
  , risk_tree_options : {
    single_object : true
    , child_options : [{
      model : null
      , list_view : GGRC.mustache_path + "/risks/tree.mustache"
      , draw_children : false
      , find_params : {
        source_type : "Risk"
      }
      , find_function : "findRelatedSource"
      , create_link : true
      , related_side : "destination"
      , parent_find_param : "destination_id"
    }, {
      model : null
      , start_expanded : true
      , draw_children : true
    }]
  }
  , getRootModelName: function() {
    return this.root_model || this.shortName;
  }
}, {
  init : function() {
    var obj_name = this.constructor.root_object;
    if(typeof obj_name !== "undefined" && this[obj_name]) {
        for(var i in this[obj_name].serialize()) {
          if(this[obj_name].hasOwnProperty(i)) {
            this.attr(i, this[obj_name][i]);
          }
        }
        this.removeAttr(obj_name);
    }

    var cache = can.getObject("cache", this.constructor, true);
    cache[this.id] = this;

    var that = this;
    this.attr("computed_errors", can.compute(function() {
      return that.errors();
    }));
  }
  , addElementToChildList : function(attrName, new_element) {
    this[attrName].push(new_element);
    this._triggerChange(attrName, "set", this[attrName], this[attrName].slice(0, this[attrName].length - 1));
  }
  , removeElementFromChildList : function(attrName, old_element, all_instances) {
    for(var i = this[attrName].length - 1 ; i >= 0; i--) {
      if(this[attrName][i]===old_element) {
        this[attrName].splice(i, 1);
        if(!all_instances) break;
      }
    }
    this._triggerChange(attrName, "set", this[attrName], this[attrName].slice(0, this[attrName].length - 1));
  }
  , refresh : function() {
    return $.ajax({
      url : this.selfLink || this.href
      , type : "get"
      , dataType : "json"
    })
    .then(can.proxy(this.constructor, "model"))
    .done(function(d) {
      d.updated();
    });
  }
  , serialize : function() {
    var that = this, serial = {};
    if(arguments.length) {
      return this._super.apply(this, arguments);
    }
    this.each(function(val, name) {
      var fun_name;
      if(that.constructor.attributes && that.constructor.attributes[name]) {
        fun_name = that.constructor.attributes[name];
        fun_name = fun_name.substr(fun_name.lastIndexOf(".") + 1);
        if(fun_name === "models") {
          serial[name] = [];
          for(var i = 0; i < val.length; i++) {
            serial[name].push(val[i].stub());
          }
        } else if(fun_name === "model") {
          serial[name] = val.stub();
        } else {
          serial[name] = that._super(name);
        }
      } else if(val && typeof val.save === "function") {
        serial[name] = val.stub();
      } else if(typeof val !== 'function') {
        serial[name] = that[name] && that[name].serialize ? that[name].serialize() : that._super(name);
      }
    });
    return serial;
  }
});

can.Observe.prototype.stub = function() {
  var type;

  if (this.constructor.getRootModelName)
    type = this.constructor.getRootModelName();
  else
    type = this.type;

  return {
    id : this.id,
    href : this.selfLink || this.href,
    type : type
  };
};

})(window.can);
