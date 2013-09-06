;(function(GGRC, can) {

  can.Construct("GGRC.ListLoaders.ListBinding", {
  }, {
      init: function(instance, loader) {
        this.instance = instance;
        this.loader = loader;

        this.list = new can.Observe.List();
        this.refresh_queue = new RefreshQueue();
        this.attach();
      }

    , attach: function() {
        this.loader.init_listeners(this);
      }

    , refresh_list: function() {
        return this.loader.refresh_list(this);
      }
  });

  can.Construct("GGRC.ListLoaders.BaseListLoader", {
      binding_factory: function(instance, loader) {
        return new GGRC.ListLoaders.ListBinding(instance, loader);
      }
  }, {
      init: function() {
      }

    , attach: function(instance) {
        return this.constructor.binding_factory(instance, this);
      }

    , insert_instance: function(binding, instance, mappings) {
        var self = this
          , found = false
          ;

        if (!(can.isArray(mappings) || mappings instanceof can.Observe.List))
          mappings = [mappings];

        can.each(binding.list, function(data, index) {
          var mapping_attr = binding.list.attr(index).attr('mappings');

          if (data.instance.id == instance.id) {
            can.each(mappings, function(mapping) {
              if (mapping_attr.indexOf(mapping) == -1) {
                mapping_attr.push(mapping);
                binding.refresh_queue.enqueue(mapping);
              }
            });
            found = true;
          }
        });
        if (!found) {
          binding.list.push({
            instance: instance,
            mappings: mappings
          });
          binding.refresh_queue.enqueue(instance);
        }
      }

    , remove_instance: function(binding, instance, mappings) {
        var self = this
          , mappings
          , mapping_index
          , instance_index_to_remove = -1
          , indexes_to_remove = []
          ;

        if (!(can.isArray(mappings) || mappings instanceof can.Observe.List))
          mappings = [mappings];

        can.each(binding.list, function(data, instance_index) {
          var mapping_attr = binding.list.attr(instance_index).attr('mappings');

          if (data.instance.id == instance.id) {
            if (mapping_attr.length == 0) {
              indexes_to_remove.push(instance_index);
            } else {
              can.each(mappings, function(mapping) {
                mapping_index = mapping_attr.indexOf(mapping);
                if (mapping_index > -1) {
                  mapping_attr.splice(mapping_index, 1);
                  if (mapping_attr.length == 0)
                    indexes_to_remove.push(instance_index);
                }
              });
            }
          }
        });
        can.each(indexes_to_remove.sort(), function(index_to_remove, count) {
          binding.list.splice(index_to_remove - count, 1);
        });
      }

  });

  GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.FilteredListLoader", {
  }, {
      init: function(source, filter_fn) {
        this._super();

        this.source = source;
        this.filter_fn = filter_fn;
      }

    , init_listeners: function(binding) {
        var self = this;

        if (this.source instanceof GGRC.ListLoaders.BaseListLoader) {
          binding.source_binding = this.source.attach(binding.instance);
        } else if (typeof(this.source) === "string") {
          // This should trigger the binding on the instance itself
          // e.g.
          // binding.instance[source]()
          // or
          // binding.instance.bindings[source]
          binding.source_binding =
            binding.instance.mappings[this.source].attach(binding.instance);
        } else {
          console.debug("Invalid source", this.source, this);
        }

        binding.source_binding.list.bind("add", function(ev, results) {
          can.each(results, function(result) {
            if (self.filter_fn(result))
              self.insert_instance(binding, result.instance, result.mappings);
          });
        });

        binding.source_binding.list.bind("remove", function(ev, results) {
          can.each(results, function(result) {
            self.remove_instance(binding, result.instance, result.mappings);
          });
        });
      }

    , refresh_list: function(binding) {
        var self = this
          , deferreds = []
          ;

        return binding.source_binding.refresh_list().then(function(results) {
          can.each(results, function(result) {
            if (self.filter_fn(result))
              self.insert_instance(binding, result.instance, result.mappings);
          });
        }).then(function() { return binding.list; });
      }
  });

  GGRC.ListLoaders.FilteredListLoader("GGRC.ListLoaders.TypeFilteredListLoader", {
  }, {
      init: function(source, model_names) {
        var filter_fn = function(result) {
          var i, model_name;
          for (i=0; i<model_names.length; i++) {
            model_name = model_names[i];
            if (typeof model_name !== 'string')
              model_name = model_name.shortName;
            if (result.instance.constructor
                && result.instance.constructor.shortName === model_name)
              return true;
          }
          return false;
        };

        this._super(source, filter_fn);
      }
  });

  GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.MultiListLoader", {
  }, {
      init: function(sources) {
        this._super();

        this.sources = sources || [];
        //this.source_bindings = [];
      }

    , init_listeners: function(binding) {
        var self = this;

        if (!binding.source_bindings)
          binding.source_bindings = [];

        can.each(this.sources, function(source) {
          var source_binding = null;
          if (source instanceof GGRC.ListLoaders.BaseListLoader) {
            source_binding = source.attach(binding.instance);
          } else if (typeof(source) === "string") {
            source_binding = binding.instance.mappings[source].attach(binding.instance);
            //source_binding = binding.instance[source]();
          }
          if (source) {
            binding.source_bindings.push(source_binding);
            self.init_source_listeners(binding, source_binding);
          }
        });
      }

    , init_source_listeners: function(binding, source) {
        var self = this;

        source.list.bind("add", function(ev, results) {
          can.each(results, function(result) {
            self.insert_instance(binding, result.instance, result.mappings);
          });
        });

        source.list.bind("remove", function(ev, results) {
          can.each(results, function(result) {
            self.remove_instance(binding, result.instance, result.mappings);
          });
        });
      }

    , refresh_list: function(binding) {
        var self = this
          , deferreds = []
          ;

        can.each(binding.source_bindings, function(source) {
          deferreds.push(
            source.refresh_list().then(function(results) {
              can.each(results, function(result) {
                self.insert_instance(binding, result.instance, result.mappings);
              });
            }));
        });

        return $.when.apply($, deferreds)
          .then(function() { return binding.list; });
      }
  });


  GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.ProxyListLoader", {
  }, {
      init: function(model_name, object_attr, option_attr,
                     object_join_attr, option_model_name) {
        this._super();

        this.model_name = model_name;
        this.object_attr = object_attr;
        this.option_attr = option_attr;
        this.object_join_attr = object_join_attr;
        this.option_model_name = option_model_name;
      }

    , init_listeners: function(binding) {
        var self = this
          , model = CMS.Models[this.model_name]
          ;

        model.bind("created", function(ev, mapping) {
          self.insert_instance_from_mapping(binding, mapping);
        });

        model.bind("destroyed", function(ev, mapping) {
          self.remove_instance_from_mapping(binding, mapping);
        });

        model.bind("orphaned", function(ev, mapping) {
          self.remove_instance_from_mapping(binding, mapping);
        });
      }

    , is_valid_mapping: function(binding, mapping) {
        var model = CMS.Models[this.model_name]
          , object_model = binding.instance.constructor
          , option_model = CMS.Models[this.option_model_name]
          ;

        return (mapping.constructor === model
                && mapping[this.object_attr]
                && (mapping[this.object_attr] === binding.instance
                    || (mapping[this.object_attr].constructor == object_model &&
                        mapping[this.object_attr].id == binding.instance.id))
                && (!option_model
                    || mapping[this.option_attr] instanceof option_model));
      }

    , get_instance_from_mapping: function(binding, mapping) {
        return mapping[this.option_attr];
      }

    , insert_instances_from_mappings: function(binding, mappings) {
        can.each(
            mappings.reverse(),
            this.proxy("insert_instance_from_mapping", binding));
        return mappings;
      }

    , insert_instance_from_mapping: function(binding, mapping) {
        var instance;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          if (instance)
            this.insert_instance(binding, instance, mapping);
        }
      }

    , remove_instance_from_mapping: function(binding, mapping) {
        var instance;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          if (instance)
            this.remove_instance(binding, instance, mapping);
        }
      }

    , refresh_list: function(binding) {
        var self = this
          , model = CMS.Models[this.model_name]
          , refresh_queue = new RefreshQueue()
          , object_join_attr = this.object_join_attr || model.table_plural
          ;

        can.each(binding.instance[object_join_attr], function(mapping) {
          refresh_queue.enqueue(mapping);
        });

        return refresh_queue.trigger()
          .then(this.proxy("insert_instances_from_mappings", binding))
          .then(function() { return binding.refresh_queue.trigger(); })
          .then(function() { return binding.list; });
      }
  });


  GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.DirectListLoader", {
  }, {
      init: function(model_name, object_attr) {
        this._super();

        this.model_name = model_name;
        this.object_attr = object_attr;
      }

    , init_listeners: function(binding) {
        var self = this
          , model = CMS.Models[this.model_name]
          ;

        model.bind("created", function(ev, mapping) {
          self.insert_instance_from_mapping(binding, mapping);
          binding.refresh_queue.trigger();
        });

        model.bind("destroyed", function(ev, mapping) {
          self.remove_instance_from_mapping(binding, mapping);
        });

        model.bind("orphaned", function(ev, mapping) {
          self.remove_instance_from_mapping(binding, mapping);
        });
      }

    , is_valid_mapping: function(binding, mapping) {
        var model = CMS.Models[this.model_name]
          , object_model = binding.instance.constructor
          ;

        return (mapping.constructor === model
                && mapping[this.object_attr]
                && (mapping[this.object_attr] === binding.instance
                    || (mapping[this.object_attr].constructor == object_model &&
                        mapping[this.object_attr].id == binding.instance.id)));
      }

    , get_instance_from_mapping: function(binding, mapping) {
        return mapping;
      }

    , insert_instances_from_mappings: function(binding, mappings) {
        can.each(mappings.reverse(), this.proxy("insert_instance_from_mapping", binding));
        return mappings;
      }

    , insert_instance_from_mapping: function(binding, mapping) {
        var instance;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          if (instance)
            this.insert_instance(binding, instance, mapping);
        }
      }

    , remove_instance_from_mapping: function(binding, mapping) {
        var instance;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          if (instance)
            this.remove_instance(binding, instance, mapping);
        }
      }

    , refresh_list: function(binding) {
        var self = this
          , model = CMS.Models[this.model_name]
          , refresh_queue = new RefreshQueue()
          , object_join_attr = this.object_join_attr || model.table_plural
          ;

        can.each(binding.instance[object_join_attr], function(mapping) {
          refresh_queue.enqueue(mapping);
        });

        return refresh_queue.trigger()
          .then(this.proxy("insert_instances_from_mappings", binding))
          .then(function() { return binding.refresh_queue.trigger(); })
          .then(function() { return binding.list; });
      }
  });
})(GGRC, can);
