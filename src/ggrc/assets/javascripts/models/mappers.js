;(function(GGRC, can) {

  /*  GGRC.ListLoaders
   *
   *  - Generates and manages lists of related objects, pairing each instance
   *      with the one or more "mappings" -- join tables, direct relationships,
   *      etc -- which cause it to be present in the list.
   *
   *  Terminology:
   *    - "mappings" -- a list of "result" objects defining the path between
   *        the root object and the paired instance; can also be the boolean
   *        literal "true", to denote the "root" instance
   *    - "result" -- the (instance, mappings) pairs
   *    - "binding" -- the pairing between a list of results and the "root"
   *        instance for that list
   *        e.g., for each item in binding.list, if you follow the chain of
   *          mappings, you will eventually find
   *            ``{ instance: binding.instance, mappings: true }``
   */
  can.Observe.List("GGRC.ListLoaders.MappingList", {
  }, {
      setup: function(mappings, options) {
        var i
          , mapping
          , mappings_as_results = []
          ;

        if (!mappings)
          mappings = [];

        for (i=0; i<mappings.length; i++) {
          mapping = mappings[i];
          if (!(mapping instanceof GGRC.ListLoaders.MappingResult))
            mapping = new GGRC.ListLoaders.MappingResult(mapping);
          mappings_as_results.push(mapping);
        }

        this._super(mappings_as_results);
      }

    , walk_instances: function(fn, last_instance) {
        can.each(this, function(mapping_result) {
          mapping_result.walk_instances(fn, last_instance);
        });
      }
  });

  /*  GGRC.ListLoaders.MappingResult
   *
   *  - `instance`: The resulting item itself
   *  - `mappings`: Essentially, the reason(s) the instance appears in the
   *      list.  This may be an instance of can.Model or a pair containing
   *      (binding, result) in the case of a chained ListLoader.
   *
   *  For FilteredListLoader, the mappings are (`result`, `binding`), where
   *    `binding` is the binding in which the result appears, and thus,
   *    `binding.loader` contains information about the filter.
   *    `binding.instance`, then, is the instance on which the original,
   *    unfiltered list is specified.
   *  For CrossListLoader, the mappings are (`result`, `binding`), where
   *    `binding` is the "remote binding" which 
   */
  can.Observe("GGRC.ListLoaders.MappingResult", {
  }, {
      setup: function(instance, mappings, binding) {
        if (!mappings) {
          // Assume item was passed in as an object
          mappings = instance.mappings;
          instance = instance.instance;
          binging = instance.binding;
        }

        if (!(mappings instanceof GGRC.ListLoaders.MappingList))
          mappings = new GGRC.ListLoaders.MappingList(mappings);

        this._super({
            instance: instance
          , mappings: mappings
          , binding: binding
        });
      }

    , walk_instances: function(fn, last_instance) {
        if (this.instance !== last_instance)
          fn(this.instance, this);
        this.mappings.walk_instances(fn, this.instance);
      }
  });

  /*  GGRC.ListLoaders.ListBinding
   */
  can.Construct("GGRC.ListLoaders.ListBinding", {
  }, {
      init: function(instance, loader) {
        this.instance = instance;
        this.loader = loader;

        this.list = new GGRC.ListLoaders.MappingList();
        this.refresh_queue = new RefreshQueue();
      }

    , refresh_list: function() {
        return this.loader.refresh_list(this);
      }

    , refresh_instance: function() {
        var refresh_queue = new RefreshQueue();
        refresh_queue.enqueue(this.instance);
        return refresh_queue.trigger();
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
        var binding = this.constructor.binding_factory(instance, this);
        this.init_listeners(binding);
        return binding;
      }

    , make_result: function(instance, mappings, binding) {
        return new GGRC.ListLoaders.MappingResult(instance, mappings, binding);
      }

    , insert_instance: function(binding, instance, mappings) {
        //console.debug("insert_instance", this.constructor.shortName, binding.name, arguments);
        var self = this
          , found_result = null
          ;

        if (!(can.isArray(mappings) || mappings instanceof can.Observe.List))
          mappings = [mappings];

        can.each(binding.list, function(data, index) {
          var mapping_attr = binding.list.attr(index).attr('mappings');

          if (data.instance.id == instance.id
              && data.instance.constructor.shortName == instance.constructor.shortName) {
            can.each(mappings, function(mapping) {
              if (mapping_attr.indexOf(mapping) == -1) {
                mapping_attr.push(mapping);
                binding.refresh_queue.enqueue(mapping.instance);
              }
            });
            found_result = data;
          }
        });
        if (!found_result) {
          found_result = this.make_result(instance, mappings, binding);
          binding.list.push(found_result);
          binding.refresh_queue.enqueue(instance);
        }
        return found_result;
      }

    , remove_instance: function(binding, instance, mappings) {
        //console.debug("remove_instance", this.constructor.shortName, binding.name, arguments);
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

          if (data.instance.id == instance.id
              && data.instance.constructor.shortName == instance.constructor.shortName) {
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

        binding.source_binding = binding.instance.get_binding(this.source);

        binding.source_binding.list.bind("add", function(ev, results) {
          can.each(results, function(result) {
            if (self.filter_fn(result))
              self.insert_instance(binding, result.instance, result);
          });
        });

        binding.source_binding.list.bind("remove", function(ev, results) {
          can.each(results, function(result) {
            self.remove_instance(binding, result.instance, result);
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
              self.insert_instance(binding, result.instance, result);
          });
        })
        .then(function() { return binding.refresh_queue.trigger(); })
        .then(function() { return binding.list; });
      }
  });

  GGRC.ListLoaders.BaseListLoader("GGRC.ListLoaders.CrossListLoader", {
  }, {
      init: function(local_mapping, remote_mapping) {
        this._super();

        this.local_mapping = local_mapping;
        this.remote_mapping = remote_mapping;
      }

    , init_listeners: function(binding) {
        var self = this;

        if (!binding.bound_insert_from_source_binding) {
          binding.bound_insert_from_source_binding =
            this.proxy("insert_from_source_binding", binding);
          binding.bound_remove_from_source_binding =
            this.proxy("remove_from_source_binding", binding);
        }

        binding.source_binding = binding.instance.get_binding(this.local_mapping);

        binding.source_binding.list.bind(
            "add", binding.bound_insert_from_source_binding);
        binding.source_binding.list.bind(
            "remove", binding.bound_remove_from_source_binding);
      }

    , insert_from_source_binding: function(binding, ev, local_results, index) {
        var self = this;
        can.each(local_results, function(local_result) {
          self.insert_local_result(binding, local_result);
        });
      }

    , remove_from_source_binding: function(binding, ev, local_results, index) {
        var self = this;
        can.each(local_results, function(local_result) {
          self.remove_local_result(binding, local_result);
        });
      }

    , insert_local_result: function(binding, local_result) {
        var self = this
          , remote_binding
          , i
          , found = false
          ;

        if (!binding.remote_bindings)
          binding.remote_bindings = [];

        for (i=0; i<binding.remote_bindings.length; i++) {
          if (binding.remote_bindings[i].instance === local_result.instance)
            return binding.remote_bindings[i];
        }

        remote_binding =
          local_result.instance.get_binding(self.remote_mapping);
        remote_binding.bound_insert_from_remote_binding =
          this.proxy("insert_from_remote_binding", binding, remote_binding);
        remote_binding.bound_remove_from_remote_binding =
          this.proxy("remove_from_remote_binding", binding, remote_binding);

        if (!binding.deferreds)
          binding.deferreds = [];

        binding.remote_bindings.push(remote_binding);

        remote_binding.refresh_instance().then(function() {
          remote_binding.list.bind(
            "add", remote_binding.bound_insert_from_remote_binding);
          remote_binding.list.bind(
            "remove", remote_binding.bound_remove_from_remote_binding);

          binding.deferreds.push(remote_binding.refresh_list());
        });

        return remote_binding;
      }

    , remove_local_result: function(binding, local_result) {
        var self = this
          , remote_binding
          , i
          , found = false
          , remote_binding_index
          ;

        if (!binding.remote_bindings)
          binding.remote_bindings = [];

        for (i=0; i<binding.remote_bindings.length; i++) {
          if (binding.remote_bindings[i].instance === local_result.instance)
            remote_binding = binding.remote_bindings[i];
        }

        if (!remote_binding) {
          console.debug("Removed binding not found:", local_result, binding);
          return;
        }

        remote_binding.list.unbind(
            "add", remote_binding.bound_insert_from_remote_binding);
        remote_binding.list.unbind(
            "remove", remote_binding.bound_remove_from_remote_binding);

        can.each(remote_binding.list, function(result) {
          self.remove_instance(binding, result.instance, result);
        });

        remote_binding_index = binding.remote_bindings.indexOf(remote_binding);
        binding.remote_bindings.splice(remote_binding_index, 1);
      }

    , insert_from_remote_binding: function(binding, remote_binding, ev, results, index) {
        var self = this;
        can.each(results, function(result) {
          inserted_result = self.insert_instance(binding, result.instance, result);
          if (!inserted_result.bindings)
            inserted_result.bindings = [];
          inserted_result.bindings.push(remote_binding);
        });
      }

    , remove_from_remote_binding: function(binding, remote_binding, ev, results, index) {
        var self = this;
        can.each(results, function(result) {
          self.remove_instance(binding, result.instance, result);
        });
      }

    , refresh_list: function(binding) {
        var self = this
          , deferreds = []
          ;

        return binding.source_binding.refresh_list().then(function(local_results) {
          can.each(local_results, function(local_result) {
            self.insert_local_result(binding, local_result);
          });
        })
        .then(function() { return $.when.apply($, binding.deferreds); })
        .then(function() { return binding.list; });
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
      }

    , init_listeners: function(binding) {
        var self = this;

        if (!binding.source_bindings)
          binding.source_bindings = [];

        can.each(this.sources, function(source) {
          var source_binding = null;
          source_binding = binding.instance.get_binding(source);
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
            self.insert_instance(binding, result.instance, result);
          });
        });

        source.list.bind("remove", function(ev, results) {
          can.each(results, function(result) {
            self.remove_instance(binding, result.instance, result);
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
                self.insert_instance(binding, result.instance, result);
              });
            }));
        });

        return $.when.apply($, deferreds)
          .then(function() { return binding.refresh_queue.trigger(); })
          .then(function() { return binding.list; });
      }
  });


  /*  ProxyListLoader
   *  - handles relationships across join tables
   *
   *  - listens to:
   *      - join_model.created
   *      - join_model.destroyed
   *      - not implemented:
   *        - join_instance.change(object_attr)
   *        - join_instance.change(option_attr)
   */
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

    , insert_instances_from_mappings: function(binding, mappings) {
        can.each(
            mappings.reverse(),
            this.proxy("insert_instance_from_mapping", binding));
        return mappings;
      }

    , insert_instance_from_mapping: function(binding, mapping) {
        var instance, result;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          result = this.get_result_from_mapping(binding, mapping);
          if (instance)
            this.insert_instance(binding, instance, result);
        }
      }

    , remove_instance_from_mapping: function(binding, mapping) {
        var instance, result;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          result = this.find_result_from_mapping(binding, mapping);
          if (instance)
            this.remove_instance(binding, instance, result);
        }
      }

    , get_result_from_mapping: function(binding, mapping) {
        return this.make_result({
            instance: mapping
          , mappings: [{
                instance: mapping[this.object_attr]
              , mappings: true
              }]
          , binding: binding
          });
      }

    , get_instance_from_mapping: function(binding, mapping) {
        return mapping[this.option_attr];
      }

    , find_result_from_mapping: function(binding, mapping) {
        var result_i, mapping_i, result;
        for (result_i=0; result_i<binding.list.length; result_i++) {
          result = binding.list[result_i];
          for (mapping_i=0; mapping_i < result.mappings.length; mapping_i++) {
            mapping_result = result.mappings[mapping_i];
            if (mapping_result.instance === mapping)
              return mapping_result;
          }
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

  /*  DirectListLoader
   *  - handles direct relationships / one-to-many relationships
   *
   *  - listens to:
   *      - model.created
   *      - model.destroyed
   *      - not implemented:
   *        - instance.change(object_attr)
   */
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

    , insert_instances_from_mappings: function(binding, mappings) {
        can.each(mappings.reverse(), this.proxy("insert_instance_from_mapping", binding));
        return mappings;
      }

    , insert_instance_from_mapping: function(binding, mapping) {
        var instance, result;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          result = this.get_result_from_mapping(binding, mapping);
          if (instance)
            this.insert_instance(binding, instance, result);
        }
      }

    , remove_instance_from_mapping: function(binding, mapping) {
        var instance;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          result = this.find_result_from_mapping(binding, mapping);
          if (instance)
            this.remove_instance(binding, instance, result);
        }
      }

    , get_result_from_mapping: function(binding, mapping) {
        return this.make_result({
            instance: mapping
          , mappings: [{
                instance: mapping[this.object_attr]
              , mappings: true
              }]
          , binding: binding
          });
      }

    , get_instance_from_mapping: function(binding, mapping) {
        return mapping;
      }

    , find_result_from_mapping: function(binding, mapping) {
        var result_i, mapping_i, result;
        for (result_i=0; result_i<binding.list.length; result_i++) {
          result = binding.list[result_i];
          for (mapping_i=0; mapping_i < result.mappings.length; mapping_i++) {
            mapping_result = result.mappings[mapping_i];
            if (mapping_result.instance === mapping)
              return mapping_result;
          }
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
