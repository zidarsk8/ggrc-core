/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

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
      init: function (model_name, object_attr, object_join_attr) {
        this._super();

        this.model_name = model_name;
        this.object_attr = object_attr;
        this.object_join_attr = object_join_attr;
      }

    , init_listeners: function (binding) {
        var self = this
          , model = CMS.Models[this.model_name] || can.Model.Cacheable
          ;

        binding.instance.bind(this.object_join_attr, function (ev, _new, _old) {
          if (binding._refresh_stubs_deferred && binding._refresh_stubs_deferred.state() !== "pending") {
            self._refresh_stubs(binding);
          }
        });

        model.bind("created", function (ev, mapping) {
          if (mapping instanceof model)
            self.filter_and_insert_instances_from_mappings(binding, [mapping]);
        });

        model.bind("destroyed", function (ev, mapping) {
          if (mapping instanceof model)
            self.remove_instance_from_mapping(binding, mapping);
        });

        model.bind("orphaned", function (ev, mapping) {
          if (mapping instanceof model)
            self.remove_instance_from_mapping(binding, mapping);
        });
      }

    , is_valid_mapping: function (binding, mapping) {
        var model = CMS.Models[this.model_name] || can.Model.Cacheable
          , object_model = binding.instance.constructor
          ;

        return (mapping instanceof model
                && mapping[this.object_attr]
                && (mapping[this.object_attr].reify() === binding.instance
                    || (mapping[this.object_attr].reify().constructor == object_model &&
                        mapping[this.object_attr].id == binding.instance.id)));
      }

    , filter_and_insert_instances_from_mappings: function (binding, mappings) {
        var self = this
          , matching_mappings
          ;

        matching_mappings = can.map(can.makeArray(mappings), function (mapping) {
          if (self.is_valid_mapping(binding, mapping))
            return mapping;
        });
        return this.insert_instances_from_mappings(binding, matching_mappings);
      }

    , insert_instances_from_mappings: function (binding, mappings) {
        var self = this
          , new_results
          ;

        new_results = can.map(can.makeArray(mappings), function (mapping) {
          return self.get_result_from_mapping(binding, mapping);
        });
        this.insert_results(binding, new_results);
      }

    , remove_instance_from_mapping: function (binding, mapping) {
        var instance;
      var result;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          result = this.find_result_from_mapping(binding, mapping);
          if (instance)
            this.remove_instance(binding, instance, result);
        }
      }

    , get_result_from_mapping: function (binding, mapping) {
        return this.make_result({
            instance: mapping
          , mappings: [{
                instance: true
              , mappings: []
              , binding: binding
              }]
          , binding: binding
          });
      }

    , get_instance_from_mapping: function (binding, mapping) {
        return mapping;
      }

    , find_result_from_mapping: function (binding, mapping) {
        var result;
        var result_i;

        for (result_i=0; result_i<binding.list.length; result_i++) {
          result = binding.list[result_i];
          if (result.instance === mapping)
            // DirectListLoader can't have multiple mappings
            return result.mappings[0];
        }
      }

    , _refresh_stubs: function (binding) {
        var that = this
          , refresh_queue = new RefreshQueue()
          ;

        refresh_queue.enqueue(binding.instance);

        return refresh_queue.trigger().then(function () {
          var object_join_attr = that.object_join_attr;
          var mappings = binding.instance[object_join_attr] && binding.instance[object_join_attr].reify();

          that.insert_instances_from_mappings(binding, mappings);
        });
      }
  });
})(window.GGRC, window.can);
