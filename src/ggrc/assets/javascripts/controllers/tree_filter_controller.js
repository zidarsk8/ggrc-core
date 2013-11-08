can.Control("GGRC.Controllers.TreeFilter", {
  
}, {
  
  init : function() {
    var parent_control;
    this._super && this._super.apply(this, arguments);
    this.options.states = new can.Observe();
    parent_control = this.element.closest(".cms_controllers_tree_view").control();
    parent_control && parent_control.options.attr("states", this.options.states);
    this.on();
  }

  , "input, select change" : function(el, ev) {
    var name = el.attr("name");
    if(el.is(".hasDatepicker")) {
      this.options.states.attr(name, moment(el.val(), "MM/DD/YYYY"));
    } else {
      this.options.states.attr(name, el.val());
    }
    ev.stopPropagation();
  }

  , "{states} change" : function(states) {
    var that = this;
    this.element
    .closest(".tree-structure")
    .children(":has(> [data-model],:data(model))").each(function(i, el) {
      var model = $(el).children("[data-model],:data(model)").data("model");
      if(can.reduce(Object.keys(states._data), function(st, key) {
        var val = states[key]
        , test = that.resolve_object(model, key);
        
        if(val && val.isAfter) {
          if(!test || !moment(test).isAfter(val)) {
            return false;
          } else {
            return st;
          }
        } else if(val && (!test || !~test.toUpperCase().indexOf(val.toUpperCase()))) {
          return false;
        } else {
          return st;
        }
      }, true)) {
        $(el).show();
      } else {
        $(el).hide();
      }
    });
  }

  , resolve_object : function(obj, path) {
    path = path.split(".");
    can.each(path, function(prop) {
      obj = obj.attr ? obj.attr(prop) : obj.prop;
      obj = obj && obj.reify ? obj.reify() : obj;
      return obj != null; //stop iterating in case of null/undefined.
    });
    return obj;
  }

  //this controller is used in sticky headers which clone the original element.
  // It should only be destroyed when the original element is destroyed, not any clone.
  , destroy : function(el, ev) {
    var sticky;
    if(this.element.is(el)) {
      this._super.apply(this, arguments);
    } else if((sticky = this.element.data("sticky")) && el.is(sticky.clone)) {
      delete sticky.clone;
    }
  }

});
