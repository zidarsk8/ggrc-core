/*
 * Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * Created By:
 * Maintained By:
 */

//= require can.jquery-all

can.Observe("can.Observe.TreeOptions", {
  defaults : {
    instance : undefined
    , parent : null
    , children_drawn : false
  }
}, {
  // init : function() {
  //   this.bind("child_options.*.list", function(ev, newVal) {
  //     this.attr("children_drawn", !newVal.length)
  //     .attr("children_drawn", !!newVal.length);
  //   });
  // }
});

can.Control("CMS.Controllers.TreeView", {
  //static properties
  defaults : {
    model : null
    , list_view : "/static/mustache/base_objects/tree.mustache"
    , parent : null
    , list : null
    , single_object : false
    , find_params : {}
    , start_expanded : false //true
    , expanded : false
    , draw_children : true
    , find_function : null
    , options_property : "tree_view_options"
    , allow_mapping : true
    , allow_creating : true
    , child_options : [] //this is how we can make nested configs. if you want to use an existing 
    //example child option :
    // { property : "controls", model : CMS.Models.Control, }
    // { parent_find_param : "system_id" ... }
  }
}, {
  //prototype properties
  setup : function(el, opts) {
    var that = this;
    typeof this._super === "function" && this._super.apply(this, [el]);
    if(opts instanceof can.Observe) {

      this.options = opts;
      if (typeof(this.options.model) === "string")
        this.options.attr("model", CMS.Models[this.options.model]);
      if(this.options.model) {
        can.each(this.options.model[opts.options_property || this.constructor.defaults.options_property], function(v, k) {
          that.options.hasOwnProperty(k) || that.options.attr(k, v);
        });
      }      
      can.each(this.constructor.defaults, function(v, k) {
        that.options.hasOwnProperty(k) || that.options.attr(k, v);
      });
    } else {
      if (typeof(opts.model) === "string")
        opts.model = CMS.Models[opts.model];
      this.options = new can.Observe(this.constructor.defaults).attr(opts.model ? opts.model[opts.options_property || this.constructor.defaults.options_property] : {}).attr(opts);
    }
  }

  , init : function(el, opts) {
    this.element.uniqueId();
    // Allow parent_instance even when there is no parent tree
    if (!this.options.parent_instance && this.options.parent)
      this.options.attr('parent_instance', this.options.parent.instance);
    this.element.trigger("loading");
    this.options.list ? this.draw_list() : this.fetch_list();

    var object_type = can.underscore(
          this.options.model ? this.options.model.shortName : "Object")
      , object_meta_type = can.underscore(window.cms_singularize(
          this.options.model ? this.options.model.root_object : "Object"))
      ;
    this.element
      .attr("data-object-type", object_type)
      .data("object-type", object_type);
    this.element
      .attr("data-object-meta-type", object_meta_type)
      .data("object-meta-type", object_meta_type);

    this.options.attr("allow_mapping_or_creating",
      this.options.allow_mapping || this.options.allow_creating);
  }

  , fetch_list : function() {
    var find_function;

    if (can.isFunction(this.options.find_params)) {
      this.options.list = this.options.find_params();
      this.draw_list();
    } else {
      if(can.isEmptyObject(this.options.find_params.serialize())) {
        this.options.find_params.attr(
          "id", this.options.parent ? this.options.parent.id : undefined);
      }

      if (this.options.mapping) {
        this.find_all_deferred =
          this.options.parent_instance.get_list_loader(this.options.mapping);
      } else if (this.options.list_loader) {
        this.find_all_deferred =
          this.options.list_loader(this.options.parent_instance);
      } else {
        if (this.options.find_function)
          find_function = this.options.find_function;
        else
          find_function = this.options.single_object ? "findOne" : "findAll";
        this.find_all_deferred =
          this.options.model[find_function](this.options.find_params.serialize());
        if (this.options.fetch_post_process)
          this.find_all_deferred =
            this.find_all_deferred.then(this.options.fetch_post_process);
      }

      this.find_all_deferred.done(this.proxy("draw_list"));
    }
  }

  , prepare_child_options: function(v) {
    //  v may be any of:
    //    <model_instance>
    //    { instance: <model instance>, mappings: [...] }
    //    <TreeOptions>
    var tmp;
    if(!(v instanceof can.Observe.TreeOptions)) {
      tmp = v;
      v = new can.Observe.TreeOptions();
      v.attr("instance", tmp);
      v.attr("start_expanded", this.options.start_expanded);
    }
    if (!(v.instance instanceof can.Model)) {
      if (v.instance.instance instanceof can.Model) {
        v.attr("mappings", v.instance.mappings);
        v.attr("instance", v.instance.instance);
      } else {
        v.attr("instance", this.options.model.model(v.instance));
      }
    }
    v.attr("child_count", can.compute(function() {
      var total_children = 0;
      if (v.attr("child_options")) {
        can.each(v.attr("child_options"), function(child_options) {
          var list = child_options.attr("list");
          if (list)
            total_children = total_children + list.length;
        });
      }
      return total_children;
    }));
    if(!v.instance.selfLink) {
      refresh_queue.enqueue(v.instance);
    }
    return v;
  }

  , draw_list : function(list) {
    var that = this;
    if(list) {
      list = list.length == null ? new can.Observe.List([list]) : list;
    } else {
      list = this.options.list;
    }

    if(!this.element)
      return;  //controller has been destroyed
    can.Observe.startBatch();
    if(!this.options.original_list) {
      this.options.attr("original_list", list);
    }
    this.options.attr("list", []);
    this.on();
    refresh_queue = new RefreshQueue();

    can.each(list, function(v, i) {
      that.options.list.push(that.prepare_child_options(v));
    });
    refresh_queue.trigger().then(function() {
      can.Observe.stopBatch();
    });
    can.view(this.options.list_view, this.options, function(frag) {
      function when_attached_to_dom(cb) {
        // Trigger the "more" toggle if the height is the same as the scrollable area
        !function poll() {
          if (!that.element) {
            return;
          } else if (that.element.closest(document.documentElement).length) {
            cb();
          }
          else {
            setTimeout(poll, 100);
          }
        }();
      }

      if (that.element) {
        that.element.html(frag);
        when_attached_to_dom(function() {
          that.element.trigger("updateCount", that.options.list.length);
          that.element.trigger("loaded");
        });
      }
      /*GGRC.queue_event(function() {
        if(that.options.start_expanded) {
          that.add_child_lists(that.options.attr("list")); //since the view is handling adding new controllers now, configure before rendering.
        }
      });*/
    });
  }

  , "{original_list} add" : function(list, ev, newVals, index) {
    var that = this;
    can.each(newVals, function(newVal) {
      that.element.trigger("newChild", newVal);
    });
    can.trigger(this.options.list, "change", "*"); //live binding isn't updating the count properly.  this forces the issue
  }
  , "{original_list} remove" : function(list, ev, oldVals, index) {
    var that = this;
    // can.each(oldVals, function(oldVal) {
    //   for(var i = that.options.list.length - 1; i >= 0; i--) {
    //     if(that.options.list[i].instance === oldVal) {
    //       that.options.list.splice(i, 1);
    //     }
    //   }
    // });
    this.options.list.splice(index, oldVals.length);
    can.trigger(this.options.list, "change", "*"); //live binding isn't updating the count properly.  this forces the issue
  }
  , "{original_list} change" : function(list, ev, newVals, index) {
    var that = this;
    if(list.isComputed) {
      this.draw_list(list());
    }
  }
  // , "{original_list} set" : function(list, ev, newVal, index) {
  //   this.options.list[index].attr("instance", newVal);
  // }

  , ".item-main expand" : function(el, ev) {
    ev.stopPropagation();
    this.options.attr('expanded', true);
    var that = this;
    var instance = el.data("model");
    var parent = can.reduce(this.options.list, function(a, b) {
      switch(true) {
        case !!a : return a;
        case b.instance === instance || b.instance === instance.instance : return b;
        default: return null;
      }
    }, null);
    if(!parent.child_options && this.options.draw_children) {
      this.add_child_lists_to_child(parent);
    }
  }

  , ".tree-structure loaded" : function(el, ev) {
    ev.stopPropagation();
    var instance_id = el.closest(".tree-item").data("object-id");
    var parent = can.reduce(this.options.list, function(a, b) {
      switch(true) {
        case !!a : return a;
        case b.instance.id === instance_id: return b;
        default: return null;
      }
    }, null);
    if(parent.children_drawn)
      return;
    parent.attr("children_drawn", true);
  }

  , ".openclose:not(.active) click" : function(el, ev) {
    // Ignore unless it's a direct child
    if (el.closest('.' + this.constructor._fullName).is(this.element))
      el.trigger("expand");
  }

  // add child options to every item (TreeViewOptions instance) in the drawing list at this level of the tree.
  , add_child_lists : function(list) {
    var that = this;
    if(that.options.draw_children) {
      //Recursively define tree views anywhere we have subtree configs.
      can.each(list, function(item) {
        that.add_child_lists_to_child(item);
      });
    }
  }

  // add all child options to one TreeViewOptions object
  , add_child_lists_to_child : function(item) {
    var that = this
      , original_child_options = this.options.child_options;
    if (original_child_options.length == null)
      child_options = [original_child_options]

    if(!item.child_options)
      item.attr("child_options", new can.Observe.TreeOptions.List());
    can.each(original_child_options, function(data, i) {
      var options = new can.Observe.TreeOptions();
      data.each(function(v, k) {
        options.attr(k, v);
      });
      that.add_child_list(item, options);
      options.attr("options_property", that.options.options_property);
      options.attr("single_object", false);
      options.attr("parent_item", item);
      // Don't allow mapping or creating unless this is the last list
      if (i < original_child_options.length - 1)
        options.attr({
          allow_mapping: false,
          allow_creating: false,
          allow_mapping_or_creating: false
        });
      GGRC.queue_event(function() {
        item.child_options.push(options);
      });
    });
  }

  // data is an entry from child options.  if child options is an array, run once for each.
  , add_child_list : function(item, data) {
    //var $subtree = $("<ul class='tree-structure'>").appendTo(el);
    //var model = $(el).closest("[data-model]").data("model");
    data.attr({ start_expanded : false, parent : item });
    var find_params;
    if(can.isFunction(item.instance[data.property])) {
      // Special case for handling mappings which are functions until
      // first requested, then set their name via .attr('...')
      find_params = function() {
        return item.instance[data.property]();
      };
      data.attr("find_params", find_params);
    } else if(data.property) {
      find_params = item.instance[data.property];
      if(find_params && find_params.isComputed) {
        data.attr("original_list", find_params);
        find_params = find_params();
      } else if(find_params && find_params.length) {
        data.attr("original_list", find_params);
        find_params = find_params.slice(0);
      }
      data.attr("list", find_params);
    } else {
      find_params = data.attr("find_params");
      if(find_params) {
        find_params = find_params.serialize();
      } else {
        find_params = {};
      }
      if(data.parent_find_param){
        find_params[data.parent_find_param] = item.instance.id;
      } else {
        find_params["parent.id"] = item.instance.id;
      }
      data.attr("find_params", new can.Observe(find_params));
    }
    // $subtree.cms_controllers_tree_view(opts);
  }

  // There is no check for parentage anymore.  When this event is triggered, it needs to be triggered
  // at the appropriate level of the tree.
  , " newChild" : function(el, ev, data) {
    this.options.list.push(this.prepare_child_options(data));
    ev.stopPropagation();
  }

  , " removeChild" : function(el, ev, data) {
    var that = this
      , instance
      , options = new can.Observe.TreeOptions();

    var model = data instanceof this.options.model
      ? data
      : new this.options.model(data.serialize ? data.serialize() : data);
    that.options.list.replace(
      can.map(
        this.options.list
        , function(v, i) {
          if(v.instance.id !== model.id) {
            return v;
          }
        })
    );
    ev.stopPropagation();
  }

  , " updateCount": function(el, ev) {
      // Suppress events from sub-trees
      if (!($(ev.target).closest('.' + this.constructor._fullName).is(this.element)))
        ev.stopPropagation();
    }

  , "{list} add": function() {
      this.element.trigger('updateCount', this.options.list.length);
    }

  , "{list} remove": function() {
      this.element.trigger('updateCount', this.options.list.length);
    }

  , " click" : function() {
    if(~this.element.text().indexOf("@@!!@@")) {
      this.draw_list();
    }
  }

  , ".edit-object modal:success" : function(el, ev, data) {
    var model = el.closest("[data-model]").data("model");
    model.attr(data[model.constructor.root_object] || data);
    ev.stopPropagation();
  }

  , ".link-object modal:success" : function(el, ev, data) {
    ev.stopPropagation();
    this.link_objects(
      el.data("child-type")
      , el.data("child-property")
      , el.closest("[data-object-id]")
      , data
    );
  }

  , " linkObject" : function(el, ev, data) {
    this.link_objects(
      data["childType"]
      , data["childProperty"]
      , this.element.children("[data-object-id=" + data["parentId"] + "]")
      , data.data
    );
  }

  , link_objects : function(child_object_type, child_property, $parent, data) {
    var that = this
    , parentid = $parent.data("object-id")
    , parent_object_type = $parent.data("object-meta-type") || window.cms_singularize($(document.body).data("page-type"))
    , $list = parentid 
        ? $parent.find(".item-content:first").children(".tree-structure[data-object-type=" + child_object_type + "]")
        : null
    , existing = parentid
        ? $list.children("[data-object-id]")
          .map(function() { return $(this).data("object-id")})
        : can.map(this.options.list, function(v, k) {
            return v.id;
          })
    , id_list = can.map(can.makeArray(data), function(v) {
      return v[parent_object_type + "_" + child_object_type][child_property];
    })
    , child_options = (parentid ? $list.control(CMS.Controllers.TreeView) : this).options
    , find_dfds = [];

    can.each(id_list, function(v) {
      //adds
      if(!~can.inArray(v, existing)) {
        find_dfds.push(child_options.model.findOne({id : v}));
      }
    })
    can.each(can.makeArray(existing), function(v) {
      //removes
      if(!~can.inArray(v, id_list)) {
        can.each(child_options.list, function(item, i) {
          if(item.id === v) {
            child_options.list.splice(i, 1);
            return false;
          }
        }) 
      }
    });

    if(find_dfds.length) {
      $.when.apply($, find_dfds).done(function() {
        var new_objs = can.makeArray(arguments);
        can.each(new_objs, function(obj) { 
          child_options.list.push(obj);
          //$list.control(CMS.Controllers.TreeView).add_child_lists($list.find("[data-object-id=" + obj.id + "]"));
        });
      });
    }

    ($list ? $list.parents(".item-content").siblings(".item-main") : this.element.children("li").children(".item-main")).openclose("open");
    if($parent && $parent.length) {
      var $box = $parent.closest(".content");
      setTimeout(function() {
        $box.scrollTop(0);
        $box.scrollTop($list.offset().top + $list.height() - $box.height() / 2);
      }, 300);
    }
  }

});
