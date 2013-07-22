(function(can, $) {

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
    //, show_view : "/static/mustache/controls/tree.mustache"
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
    this.fetch_list({});
  }

  , fetch_list : function(params) {
    if(this.options.is_related) {
      // FIXME: This should use 'object_type' and 'other_type', once the server
      // supports it, e.g. to support dual and symmetric relationships
      this.options.model.findRelated({
          source_id : this.options.parent_id
        , source_type : this.options.parent_type
        , destination_type : this.options.object_type
      }).done(this.proxy('draw_list'));
    } else {
      this.options.model.findAll(params, this.proxy('draw_list'));
    }
  }

  , draw_list : function(list) {
    var that = this;
    if(list) {
      this.options.list = list;
    }
    can.view(this.options.list_view, this.options, function(frag) {
      that.element
        .html(frag)
        .trigger("updateCount", that.options.list.length);
    });
  }

  , "{model} created" : function(Model, ev, instance) {
    if(this.options.model === Model && !this.options.is_related) {
      this.options.list.unshift(instance);
    }
  }
});

})(this.can, this.can.$);
