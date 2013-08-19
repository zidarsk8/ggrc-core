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

var all_relationships_as_source = null
  , all_relationships_as_destination = null;

function related_model_list_loader(controller) {
  var list = new can.Observe.List()
    , refresh_queue = new RefreshQueue()
    , parent = controller.options.parent_instance
    , parent_type = controller.options.parent_type
    , parent_id = controller.options.parent_id
    , object_type = controller.options.object_type
    ;

  function insert_instance(instance) {
    if (list.indexOf(instance) == -1) {
      refresh_queue.enqueue(instance);
      list.unshift(instance);
    }
  }

  function remove_instance(instance) {
    var index = list.indexOf(instance);

    if (index > -1)
      list.splice(index, 1);
  }

  function insert_related_instance(relationship) {
    if (relationship.destination.constructor.shortName == object_type
        && (relationship.source === parent
            || (relationship.source_type === parent_type
                && relationship.source_id === parent_id)))
      insert_instance(relationship.destination);
    if (relationship.destination.constructor.shortName == object_type
        && (relationship.destination === parent
            || (relationship.destination_type === parent_type
                && relationship.destination_id === parent_id)))
      insert_instance(relationship.source);
  }

  function insert_related_instances(relationships) {
    can.each(relationships.reverse(), insert_related_instance);
  }

  // Should collate relationships by `relationship_type` and fetch both
  // as source and as destination

  CMS.Models.Relationship.bind("created", function(ev, instance) {
    if (instance.constructor == CMS.Models.Relationship) {
      insert_related_instance(instance);
    }
  });

  if (!all_relationships_as_source)
    all_relationships_as_source = CMS.Models.Relationship.findAll({
        source_id : parent_id
      , source_type : parent_type
    })
  if (!all_relationships_as_destination)
    all_relationships_as_destination = CMS.Models.Relationship.findAll({
        destination_id : parent_id
      , destination_type : parent_type
    })

  return $
    .when(
        all_relationships_as_source.then(insert_related_instances)
      , all_relationships_as_destination.then(insert_related_instances))
    .then(refresh_queue.proxy("trigger"))
    .then(function() { return list });

  return $.when(
      CMS.Models.Relationship.findAll({
      //controller.options.model.findRelated({
          source_id : parent_id
        , source_type : parent_type
        , destination_type : object_type
        }).then(insert_related_instances)
    , //controller.options.model.findRelated({
      CMS.Models.Relationship.findAll({
          destination_id : parent_id
        , destination_type : parent_type
        , source_type : object_type
        }).then(insert_related_instances))
    .then(refresh_queue.proxy("trigger"))
    .then(function() {
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

    if (!this.options.list_loader) {
      if (this.options.is_related)
        this.options.list_loader = related_model_list_loader;
      else
        this.options.list_loader = model_list_loader;
    }
    this.fetch_list({});
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
