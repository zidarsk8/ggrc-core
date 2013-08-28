(function(can, $) {

function model_list_loader(controller) {
  var list = new can.Observe.List();

  function insert_instance(instance) {
    if (list.indexOf(instance) == -1) {
      list.unshift(instance);
    }
  }

  function remove_instance(instance) {
    var index = list.indexOf(instance);

    if (index > -1)
      list.splice(index, 1);
  }

  controller.options.model.bind("created", function(ev, instance) {
    insert_instance(instance);
  });

  return controller.options.model.findAll().then(function(instances) {
    can.each(instances.reverse(), function(instance) {
      if (instance.constructor == controller.options.model)
        insert_instance(instance);
    });
    return list;
  });
}

can.Control("GGRC.Controllers.ListView", {
  defaults : {
    is_related : false
    , model : null
    , parent_instance : null
    , object_type : null
    , parent_type : null
    , object_display : null
    , parent_display : null
    , list_view : "/static/mustache/dashboard/object_list.mustache"
    , list_objects : null
    , list_loader : null
    , tooltip_view : "/static/mustache/dashboard/object_tooltip.mustache"
  }
}, {

  init : function() {
    if(this.options.is_related) {
      if (!this.options.parent_instance)
        this.options.parent_instance = GGRC.make_model_instance(GGRC.page_object);
      if(!this.options.parent_type)
        this.options.parent_type = this.options.parent_instance.constructor.shortName;

      if(this.options.parent_id == null)
        this.options.parent_id = this.options.parent_instance.id;
    } else {
      this.on();  //set up created listener for model
    }

    if(this.options.is_related) {
      if(this.options.object_type !== "system_process") {
        this.options.object_display =
          this.options.object_route.split("_").map(can.capitalize).join(" ");
      }
      this.options.object_type =
        this.options.object_type.split("_").map(can.capitalize).join("");
      this.options.parent_display =
        this.options.parent_type.split("_").map(can.capitalize).join(" ");
    }

    if (this.options.list) {
      this.draw_list(this.options.list);
    } else {
      if (!this.options.list_loader) {
        if (this.options.is_related)
          this.options.list_loader = related_model_list_loader;
        else
          this.options.list_loader = model_list_loader;
      }
      this.fetch_list({});
    }
  }

  , fetch_list : function(params) {
    this.element.trigger("loading");
    this.options.list_loader(this).then(this.proxy("draw_list"));
  }

  , draw_list : function(list) {
    var that = this;
    if(list) {
      this.options.list = list;
      this.on();
    }
    can.view(this.options.list_view, this.options, function(frag) {
      that.element
        .html(frag)
        .trigger("loaded")
        .trigger("updateCount", that.options.list.length);
    });
  }

  , update_count: function() {
      this.element.trigger("updateCount", this.options.list.length).trigger("widget_updated");
    }

  , "{list} change": "update_count"
});

})(this.can, this.can.$);
