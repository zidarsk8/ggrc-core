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
      return this.makeResult({
        instance: mapping.reify(),
        mappings: [{
          instance: mapping,
          mappings: [{
            instance: true,
            mappings: [],
            binding: binding
          }],
          binding: binding
        }]
      });
    },
    makeResult: function (instance, mappings, binding) {
      return new GGRC.ListLoaders.MappingResult(instance, mappings, binding);
    }
  });
})(GGRC, can);
