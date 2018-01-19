/*
 Copyright (C) 2018 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can) {
  /*  IndirectListLoader
   *  - handles indirect relationships
   *  (zero-to-many, no local join but has a direct mapping in another object)
   *
   *  - listens to:
   *      - model.created
   *      - model.destroyed
   *      - not implemented:
   *        - instance.change(object_attr)
   */
  GGRC.ListLoaders.BaseListLoader('GGRC.ListLoaders.IndirectListLoader', {}, {
    init: function (modelName, objectAttr) {
      this._super();

      this.model_name = modelName;
      this.object_attr = objectAttr;
    },
    init_listeners: function (binding) {
      var self = this;
      var model = CMS.Models[this.model_name];

      model.bind('created', function (ev, mapping) {
        if (mapping instanceof model)
          self.filter_and_insert_instances_from_mappings(binding, [mapping]);
      });

      model.bind('destroyed', function (ev, mapping) {
        if (mapping instanceof model)
          self.remove_instance_from_mapping(binding, mapping);
      });

      model.bind('orphaned', function (ev, mapping) {
        if (mapping instanceof model)
          self.remove_instance_from_mapping(binding, mapping);
      });
    },
    is_valid_mapping: function (binding, mapping) {
      var model = CMS.Models[this.model_name];
      var objectModel = binding.instance.constructor;

      return (mapping instanceof model && mapping[this.object_attr] &&
      (mapping[this.object_attr].reify() === binding.instance ||
      (mapping[this.object_attr].type === 'Context' ||
      (mapping[this.object_attr].reify() &&
      mapping[this.object_attr].reify().constructor === objectModel) &&
      mapping[this.object_attr].id === binding.instance.id)));
    },
    filter_and_insert_instances_from_mappings: function (binding, mappings) {
      var self = this;
      var matchingMappings;

      matchingMappings = can.map(can.makeArray(mappings), function (mapping) {
        if (self.is_valid_mapping(binding, mapping))
          return mapping;
      });
      return this.insert_instances_from_mappings(binding, matchingMappings);
    },
    insert_instances_from_mappings: function (binding, mappings) {
      var self = this;
      var newResults;

      newResults = can.map(can.makeArray(mappings), function (mapping) {
        return self.get_result_from_mapping(binding, mapping);
      });
      this.insert_results(binding, newResults);
    },
    remove_instance_from_mapping: function (binding, mapping) {
      var instance;
      var result;
      if (this.is_valid_mapping(binding, mapping)) {
        instance = this.get_instance_from_mapping(binding, mapping);
        result = this.find_result_from_mapping(binding, mapping);
        if (instance)
          this.remove_instance(binding, instance, result);
      }
    },
    get_result_from_mapping: function (binding, mapping) {
      return this.make_result({
        instance: mapping,
        mappings: [{
          instance: true,
          mappings: [],
          binding: binding
        }],
        binding: binding
      });
    },
    get_instance_from_mapping: function (binding, mapping) {
      return mapping;
    },
    find_result_from_mapping: function (binding, mapping) {
      var result;
      var resultInd;

      for (resultInd = 0; resultInd < binding.list.length; resultInd++) {
        result = binding.list[resultInd];
        if (result.instance === mapping)
        // DirectListLoader can't have multiple mappings
          return result.mappings[0];
      }
    },
    _refresh_stubs: function (binding) {
      var model = CMS.Models[this.model_name];
      var objectJoinAttr =
        ('indirect_' + (this.object_join_attr || model.table_plural));
      var mappings = binding.instance[objectJoinAttr] &&
        binding.instance[objectJoinAttr].reify();
      var params = {};
      var objectAttr = this.object_attr +
        (this.object_attr !== 'context' &&
        model.attributes[this.object_attr].indexOf('stubs') > -1 ?
          '.id' : '_id');
      var result;
      var self = this;

      params[objectAttr] =
        this.object_attr === 'context' ?
        binding.instance.context && binding.instance.context.id :
          binding.instance.id;

      if (mappings || !params[objectAttr]) {
        this.insert_instances_from_mappings(binding, mappings);
        result = new $.Deferred().resolve(mappings);
      } else {
        result = model.findAll(params).done(function (mappings) {
          // binding.instance.attr(object_join_attr, mappings);
          self.insert_instances_from_mappings(binding, mappings.reify());
        });
      }
      return result;
    },
    refresh_list: function () {
      return this._refresh_stubs();
    }
  });
})(window.GGRC, window.can);
