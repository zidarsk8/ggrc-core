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

  root_object : ""
  , root_collection : ""
  , model_singular : ""
  , model_plural : ""
  , table_singular : ""
  , table_plural : ""
  , title_singular : ""
  , title_plural : ""
  , findOne : "GET {href}"
  , setup : function(construct, name, statics, prototypes) {
    var overrideFindAll = false;
    if(this.fullName === "can.Model.Cacheable") {
      this.findAll = function() {
        throw "No default findAll() exists for subclasses of Cacheable";
      };
    }
    else if((!statics || !statics.findAll) && this.findAll === can.Model.Cacheable.findAll) { 
      if(this.root_collection) {
        this.findAll = "GET /api/" + this.root_collection;
      } else {
        overrideFindAll = true;
      }
    }
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

    var ret = this._super.apply(this, arguments);
    if(overrideFindAll)
      this.findAll = can.Model.Cacheable.findAll;
    return ret;
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
      var href = params.selfLink || params.href;

      if (href)
        return _refresh.call(this, {href : params.selfLink || params.href});
      else
        return (new can.Deferred()).reject();
    };

    var that = this;
    this.risk_tree_options = can.extend(true, {}, this.risk_tree_options); //for subclasses
    var risk_child_options = that.risk_tree_options.child_options[0];
    this.risk_tree_options.show_view = GGRC.mustache_path + "/base_objects/tree.mustache";
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

    this.init_mappings();
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
    if (!params || params.length == 0)
      return new this.List();
    var ms = this._super(params);
    if(params instanceof can.Observe) {
      params.replace(ms);
      return params;
    } else {
      return ms;
    }
  }
  , object_from_resource : function(params) {
      var obj_name = this.root_object;
      if(!params) {
        return params;
      }
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
      return params;
    }
  , model : function(params) {
    var m, that = this;
    params = this.object_from_resource(params);
    if (!params)
      return params;
    var fn = (typeof params.each === "function") ? can.proxy(params.each,"call") : can.each;
    if(m = this.findInCacheById(params.id)) {
      if (m === params) {
        //return m;
      } else if (!params.selfLink) {
        //return m;
      } else {
      if (!m.selfLink) {
        //we are fleshing out a stub, which is much like creating an object new.
        //But we don't want to trigger every change event on the new object's props.
        m._init = 1;
        // Stub attributes should be removed to not conflict with real model
        // attributes; however, this should be well-tested first
        //m.removeAttr('type');
        //m.removeAttr('href');
      }
      fn(params, function(val, key) {
        var i = 0, j = 0, k, changed = false;
        if(m[key] instanceof can.Observe.List) {
          if (changed === false) {
            for (i=0; changed === false && i < m[key].length; i++) {
              // If m[key][i] === val[i] then they're the same
              // If val[i] is a stub of m[key][i], then it provides no new data
              if (!(m[key][i] === val[i]
                    || (val[i] && !val[i].selfLink && m[key][i].id === val[i].id
                        && m[key][i].constructor.shortName === val[i].type)))
                changed = i;
            }
          }
          if (changed === false && m[key].length < val.length)
            changed = m[key].length;
          if (changed !== false) {
            var p = val && val.serialize ? val.serialize() : val;
            p = p.slice(changed);
            m[key].splice.apply(m[key], [changed, m[key].length - changed].concat(
              m[key].constructor.models ?
                can.makeArray(m[key].constructor.models(p))
                : p));
          }
          // TODO -- experimental list optimization below -- BM 7/15/2013
          // p = m[key].constructor.models ? m[key].constructor.models(p) : p;
          // while(i < m[key].length && j < p.length) {
          //   if(m[key][i] === p[j]) {
          //     i++; j++;
          //   } else if((k = can.inArray(m[key][i], p)) > j) {
          //     m[key].splice(i, 0, p.slice(j, k - j));
          //     i += k - j + 1;
          //     j = k + 1;
          //   } else if((k = can.inArray(p[j], m[key])) > i) {
          //     m[key].splice(i, k - i);
          //     i++;
          //     j++;
          //   } else {
          //     m[key].splice(i, 1);
          //   }
          // }
          // i = m[key].length;
          // j = p.length;
          // if(i < j) {
          //   m[key].splice(i, 0, p.slice(i, j - i));
          // } else if(j < i) {
          //   m[key].splice(j, i - j);
          // }
        } else if(m[key] instanceof can.Model) {
          if (!(m[key] === val
              || (val && !val.selfLink && m[key].id === val.id
                  && m[key].constructor.shortName === val.type))) {
            if (val == null)
              m.removeAttr(key);
            else
              m[key].constructor.model(params[key] || {});
          }
        } else {
          if (val == null)
            m.removeAttr(key)
          else
            m.attr(key, val && val.serialize ? val.serialize() : val);
        }
      });
      delete m._init;
      }
    } else {
      fn(params, function(val, key) {
        if (val == null) {
          if (params.removeAttr)
            params.removeAttr(key);
          else
            delete params[key];
        }
      });
      m = this._super(params);
    }
    return m;
  }
  , tree_view_options : {}
  , risk_tree_options : {
    single_object : true
    , child_options : [{
      model : null
      , show_view : GGRC.mustache_path + "/risks/tree.mustache"
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
      , start_expanded : false
      , draw_children : true
    }]
  }
  , getRootModelName: function() {
    return this.root_model || this.shortName;
  }

  , init_mappings: function() {
      var self = this;
      can.each(this.mappings, function(options, name) {
        self.define_association_proxy(name, options);
      });
    }

  , define_association_proxy: function(name, options) {
      /* Adds association proxy methods to prototype
       */
      var attr = options.attr
        , target_attr = options.target_attr
        , update_function_name = "_update_" + name
        , update_function
        , change_handler_name = "_handle_changed_" + name
        , change_handler
        , init_flag_name = "_initialized_" + name
        ;

      update_function = function() {
        var self = this
          , refresh_queue = new RefreshQueue()
          ;

        can.each(self[attr], function(mapping) {
          refresh_queue.enqueue(mapping);
        });
        return refresh_queue.trigger()
          .then(function(mappings) {
            var refresh_queue = new RefreshQueue();
            can.each(mappings, function(mapping) {
              refresh_queue.enqueue(mapping[target_attr]);
            });
            return refresh_queue.trigger()
              .then(function(mapped_objects) {
                self[name].replace(
                  can.map(mappings, function(mapping) {
                    if (mapping[target_attr] && mapping[target_attr].selfLink)
                      return {
                          instance: mapping[target_attr]
                        , mappings: [mapping]
                      };
                  }));
              });
          });
      };

      this.prototype[update_function_name] = update_function;

      change_handler = function(ev, attr, how) {
        var self = this;
        if(this[init_flag_name] && /^(?:\d+)?(?:\.updated)?$/.test(attr)) {
          //self[update_function_name]();
          setTimeout(self.proxy(update_function_name), 10);
        }
      };

      this.prototype[change_handler_name] = change_handler;

      if (!this.prototype._init_mappings) {
        this.prototype._init_mappings = function() {
          var self = this;
          can.each(this.constructor.mappings_init_functions, function(fn) {
            fn.apply(self);
          });
        }
      }

      this.prototype[name] = function() {
        this[init_flag_name] = true;
        if (!this.attr(name))
          this[name] = new can.Observe.List();
        this[update_function_name]();
        this[attr].bind("change", this.proxy(change_handler_name));
        return this[name];
      }
      /*if (!this.mappings_init_functions)
        this.mappings_init_functions = [];

      this.mappings_init_functions.push(function() {
        if (!this[name])
          this[name] = new can.Observe.List();
        this[attr].bind("change", this.proxy(change_handler_name));
      });*/
    }
}, {
  init : function() {
    var cache = can.getObject("cache", this.constructor, true);
    if (this.id)
      cache[this.id] = this;
  }
  , computed_errors : function() {
      var that = this
        , compute = can.compute(function() { return that.errors(); });
      return compute;
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
  , refresh : function(params) {
    var href = this.selfLink || this.href;

    if (!href)
      return (new can.Deferred()).reject();
    return $.ajax({
      url : href
      , params : params
      , type : "get"
      , dataType : "json"
    })
    .then(can.proxy(this.constructor, "model"))
    /*.done(function(d) {
      d.updated();
      //can.trigger(d, "change", "*"); //more complete refresh than triggering "updated" like we used to, but will performance suffer?
    });*/
  }
  , attr : function() {
    if(arguments.length < 1) {
      return this.serialize();  // Short-circuit CanJS's "attr"-based serialization which leads to infinite recursion
    } else {
      return this._super.apply(this, arguments);
    }
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
        if(fun_name === "models" || fun_name === "get_instances") {
          serial[name] = [];
          for(var i = 0; i < val.length; i++) {
            serial[name].push(val[i].stub());
          }
        } else if(fun_name === "model" || fun_name === "get_instance") {
          serial[name] = (val ? val.stub() : null);
        } else {
          serial[name] = that._super(name);
        }
      } else if(val && typeof val.save === "function") {
        serial[name] = val.stub();
      } else if(typeof val === "object" && val != null && val.length != null) {
        serial[name] = can.map(val, function(v) {
          return (v && typeof v.save === "function") ? v.stub() : (v.serialize ? v.serialize() : v);
        });
      } else if(typeof val !== 'function') {
        serial[name] = that[name] && that[name].serialize ? that[name].serialize() : that._super(name);
      }
    });
    return serial;
  }
  , display_name : function() {
    return this.title || this.name;
  }
});

can.Observe.prototype.stub = function() {
  var type;

  if (this.constructor.shortName)
    type = this.constructor.shortName;
  else
    type = this.type;

  if (!this.id)
    return null;

  return {
    id : this.id,
    href : this.selfLink || this.href,
    type : type
  };
};

})(window.can);
