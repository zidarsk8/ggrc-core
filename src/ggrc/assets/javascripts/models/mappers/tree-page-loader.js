/*!
 Copyright (C) 2016 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

;(function (GGRC, can) {
  'use strict';

  GGRC.ListLoaders.BaseListLoader('GGRC.ListLoaders.TreePageLoader', {}, {
    init: function (model, instance, mapping) {
      this.model = model;
      this.binding = instance.get_binding(mapping);
    },
    load: function (params) {
      return this.model.query(params)
        .then(function (data) {
          data.values = this.insertInstancesFromMappings(data.values);
          return data;
        }.bind(this));
    },
    insertInstancesFromMappings: function (mappings) {
      var self = this;
      var result;

      result = can.map(can.makeArray(mappings), function (mapping) {
        return self.getResultFromMapping(mapping);
      });
      return new can.List(result);
    },
    getResultFromMapping: function (mapping) {
      var binding = this.binding;
      return this.makeResult(mapping.reify(), binding);
    },
    makeResult: function (instance, binding) {
      var relationship =
        GGRC.Utils.getRelationshipBetweenInstances(binding.instance, instance);
      return new GGRC.ListLoaders.MappingResult(instance, [
        {
          binding: binding,
          instance: relationship,
          mappings: [{
            instance: true,
            mappings: [],
            binding: binding
          }]
        }
      ], binding);
    }
  });
})(GGRC, can);
