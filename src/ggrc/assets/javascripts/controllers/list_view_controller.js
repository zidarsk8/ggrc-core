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

can.Construct("GGRC.ListLoaders.BaseListLoader", {
}, {
    init: function() {
      this.list = new can.Observe.List();
      this.refresh_queue = new RefreshQueue();
    }

  , insert_instance: function(instance, mapping) {
      var self = this
        , found = false
        ;

      can.each(this.list, function(data, index) {
        if (data.instance.id == instance.id) {
          self.list.attr(index).attr('mappings').push(mapping);
          self.refresh_queue.enqueue(mapping);
          found = true;
        }
      });
      if (!found) {
        this.list.push({
          instance: instance,
          mappings: [mapping]
        });
        self.refresh_queue.enqueue(instance);
      }
    }

  , remove_instance: function(instance, mapping) {
      var self = this
        , mappings
        , mapping_index
        , instance_index_to_remove = -1
        ;

      can.each(this.list, function(data, index) {
        if (data.instance.id == instance.id) {
          mappings = self.list.attr(index).attr('mappings');
          mapping_index = mappings.indexOf(mapping);
          if (mapping_index > -1) {
            mappings.splice(mapping_index, 1);
            if (mappings.length == 0)
              instance_index_to_remove = index;
          }
        }
      });
      if (instance_index_to_remove > -1)
        this.list.splice(instance_index_to_remove, 1);
    }

});


GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.ProxyListLoader", {
}, {
    init: function(parent_instance, model_name,
              object_attr, option_attr, object_join_attr, option_model_name) {
      this._super();

      this.parent_instance = parent_instance;

      this.model_name = model_name;
      this.object_attr = object_attr;
      this.option_attr = option_attr;
      this.object_join_attr = object_join_attr;
      this.option_model_name = option_model_name;

      this.object_type = this.parent_instance.constructor.shortName;

      this.init_bindings();
    }

  , init_bindings: function() {
      var self = this
        , model = CMS.Models[this.model_name]
        ;

      model.bind("created", function(ev, mapping) {
        self.refresh_queue = new RefreshQueue();
        self.insert_instance_from_mapping(mapping);
        self.refresh_queue.trigger();
      });

      model.bind("destroyed", function(ev, mapping) {
        self.remove_instance_from_mapping(mapping);
      });
    }

  , is_valid_mapping: function(mapping) {
      var model = CMS.Models[this.model_name]
        , object_model = this.parent_instance.constructor
        , option_model = CMS.Models[this.option_model_name]
        ;

      return (mapping.constructor === model
              && (mapping[this.object_attr] === this.parent_instance
                  || (mapping[this.object_attr].constructor == object_model &&
                      mapping[this.object_attr].id == this.parent_instance.id))
              && mapping[this.option_attr] instanceof option_model);
    }

  , get_instance_from_mapping: function(mapping) {
      return mapping[this.option_attr];
    }

  , insert_instances_from_mappings: function(mappings) {
      can.each(mappings.reverse(), this.proxy("insert_instance_from_mapping"));
      return mappings;
    }

  , insert_instance_from_mapping: function(mapping) {
      var instance;
      if (this.is_valid_mapping(mapping)) {
        instance = this.get_instance_from_mapping(mapping);
        if (instance)
          this.insert_instance(instance, mapping);
      }
    }

  , remove_instance_from_mapping: function(mapping) {
      var instance;
      if (this.is_valid_mapping(mapping)) {
        instance = this.get_instance_from_mapping(mapping);
        if (instance)
          this.remove_instance(instance, mapping);
      }
    }

  , refresh_list: function() {
      var self = this
        , model = CMS.Models[this.model_name]
        , refresh_queue = new RefreshQueue()
        , object_join_attr = this.object_join_attr || model.table_plural
        ;

      can.each(this.parent_instance[object_join_attr], function(mapping) {
        refresh_queue.enqueue(mapping);
      });

      return refresh_queue.trigger()
        .then(this.proxy("insert_instances_from_mappings"))
        .then(function() { return self.refresh_queue.trigger(); })
        .then(function() { return self.list; });
    }
});

GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.RelatedListLoader", {
    init_relationships: function(parent_instance) {
      var parent_id = parent_instance.id
        , parent_type = parent_instance.constructor.shortName
        ;

      if (!this.all_relationships_as_source)
        this.all_relationships_as_source = CMS.Models.Relationship.findAll({
            source_id : parent_id
          , source_type : parent_type
        });

      if (!this.all_relationships_as_destination)
        this.all_relationships_as_destination = CMS.Models.Relationship.findAll({
            destination_id : parent_id
          , destination_type : parent_type
        });
    }
}, {
    init: function(parent_instance, object_type) {
      this._super();

      this.parent_instance = parent_instance;
      this.object_type = object_type;

      this.parent_type = parent_instance.constructor.shortName;
      this.parent_id = parent_instance.id;

      this.init_bindings();
    }

  , get_related_instance: function(relationship) {
      if (relationship.destination.constructor.shortName == this.object_type
          && (relationship.source === this.parent_instance
              || (relationship.source_type === this.parent_type
                  && relationship.source_id === this.parent_id)))
        return relationship.destination;
      else if (relationship.source.constructor.shortName == this.object_type
          && (relationship.destination === this.parent_instance
              || (relationship.destination_type === this.parent_type
                  && relationship.destination_id === this.parent_id)))
        return relationship.source;
    }

  , insert_related_instance: function(relationship) {
      var instance = this.get_related_instance(relationship);
      if (instance)
        this.insert_instance(instance, relationship);
    }

  , insert_related_instances: function(relationships) {
      can.each(relationships.reverse(), this.proxy("insert_related_instance"));
    }

  , remove_related_instance: function(relationship) {
      var instance = this.get_related_instance(relationship);
      if (instance)
        this.remove_instance(instance, relationship);
    }

  , init_bindings: function() {
      var self = this;

      CMS.Models.Relationship.bind("created", function(ev, instance) {
        if (instance.constructor == CMS.Models.Relationship) {
          self.insert_related_instance(instance);
        }
      });

      CMS.Models.Relationship.bind("destroyed", function(ev, instance) {
        if (instance.constructor == CMS.Models.Relationship) {
          self.remove_related_instance(instance);
        }
      });
    }

  , refresh_list: function() {
      var self = this;

      this.constructor.init_relationships(this.parent_instance);

      return $.when(
          this.constructor.all_relationships_as_source
            .then(this.proxy("insert_related_instances"))
        , this.constructor.all_relationships_as_destination
            .then(this.proxy("insert_related_instances"))
        )
        .then(this.refresh_queue.proxy("trigger"))
        .then(function() { return self.list });
    }
});

function related_model_list_loader(controller) {
  var parent_instance = controller.options.parent_instance
    , parent_type = parent_instance.constructor.shortName
    , object_type = controller.options.object_type
    , loader;

  loader = new GGRC.ListLoaders.RelatedListLoader(
    controller.options.parent_instance, controller.options.object_type);

  return loader.refresh_list();
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
