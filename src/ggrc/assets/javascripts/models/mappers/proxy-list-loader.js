/*!
    Copyright (C) 2016 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (GGRC, can) {
  'use strict';

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
      init: function (model_name, object_attr, option_attr,
                     object_join_attr, option_model_name) {
        this._super();

        this.model_name = model_name;
        this.object_attr = object_attr;
        this.option_attr = option_attr;
        this.object_join_attr = object_join_attr;
        this.option_model_name = option_model_name;
      }

    , init_listeners: function (binding) {
        var self = this
          , model = CMS.Models[this.model_name]
          , object_join_value = binding.instance[this.object_join_attr]
          ;

        binding.instance.bind(this.object_join_attr, function (ev, _new, _old) {
          if (binding._refresh_stubs_deferred && binding._refresh_stubs_deferred.state() !== "pending")
            self._refresh_stubs(binding);
        });

        if (object_join_value) {
          object_join_value.bind('length', function (ev, _new, _old) {
            self._refresh_stubs(binding);
          });
        }

        model.bind("created", function (ev, mapping) {
          if (mapping instanceof model)
            self.filter_and_insert_instances_from_mappings(binding, [mapping]);
        });

        model.bind("destroyed", function (ev, mapping) {
          if (mapping instanceof model)
            self.remove_instance_from_mapping(binding, mapping);
        });

        //  FIXME: This is only needed in DirectListLoader, right?
        model.bind("orphaned", function (ev, mapping) {
          if (mapping instanceof model)
            self.remove_instance_from_mapping(binding, mapping);
        });
      }

    , is_valid_mapping: function (binding, mapping) {
        var model = CMS.Models[this.model_name]
          , object_model = binding.instance.constructor
          , option_model = CMS.Models[this.option_model_name]
          ;

        return (mapping.constructor === model
                && mapping[this.object_attr]
                && (mapping[this.object_attr].reify() === binding.instance
                    || (mapping[this.object_attr].reify().constructor == object_model &&
                        mapping[this.object_attr].id == binding.instance.id))
                && (!option_model
                    || (mapping[this.option_attr]
                        && mapping[this.option_attr].reify() instanceof option_model)));
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
        var instance, result;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          result = this.find_result_from_mapping(binding, mapping);
          if (instance)
            this.remove_instance(binding, instance, result);
        }
      }

    , get_result_from_mapping: function (binding, mapping) {
        return this.make_result({
            instance: mapping[this.option_attr].reify()
          , mappings: [{
                instance: mapping
              , mappings: [{
                    instance: true
                  , mappings: []
                  , binding: binding
                  }]
              , binding: binding
              }]
          });
      }

    , get_instance_from_mapping: function (binding, mapping) {
        return mapping[this.option_attr] && mapping[this.option_attr].reify();
      }

    , find_result_from_mapping: function (binding, mapping) {
        var mapping_i;
        var result;
        var result_i;
      var mapping_result;

        for (result_i=0; result_i<binding.list.length; result_i++) {
          result = binding.list[result_i];
          for (mapping_i=0; mapping_i < result.mappings.length; mapping_i++) {
            mapping_result = result.mappings[mapping_i];
            if (mapping_result.instance === mapping)
              return mapping_result;
          }
        }
      }

    , _refresh_stubs: function (binding) {
        var model = CMS.Models[this.model_name];
        var refresh_queue = new RefreshQueue();
        var object_join_attr = this.object_join_attr || model.table_plural;

        // These properties only exist if the user has read access
        if (binding.instance[object_join_attr]) {
          can.each(binding.instance[object_join_attr].reify(), function (mapping) {
            refresh_queue.enqueue(mapping);
          });
        }

        return refresh_queue.trigger()
          .then(this.proxy("filter_for_valid_mappings", binding))
          .then(this.proxy("insert_instances_from_mappings", binding));
      }

    , filter_for_valid_mappings: function (binding, mappings) {
        // Remove incomplete mappings, including those not in our context
        //   (which the server refused to provide).
        var i
          , valid_mappings = [];

        for (i=0; i<mappings.length; i++) {
          if (mappings[i][this.option_attr])
            valid_mappings.push(mappings[i]);
        }
        return valid_mappings;
      }
  });
})(window.GGRC, window.can);
