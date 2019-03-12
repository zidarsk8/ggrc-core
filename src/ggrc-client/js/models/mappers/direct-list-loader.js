/*
 Copyright (C) 2019 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

import RefreshQueue from '../refresh_queue';
import Cacheable from '../cacheable';
import {Person, Cycle} from '../business-models';
import {reify} from '../../plugins/utils/reify-utils';
import {Role} from '../service-models';

const directListModels = {
  Person,
  Cycle,
  Role,
};

(function (GGRC, can) {
  /*  DirectListLoader
   *  - handles direct relationships / one-to-many relationships
   *
   *  - listens to:
   *      - model.created
   *      - model.destroyed
   *      - not implemented:
   *        - instance.change(object_attr)
   */
  GGRC.ListLoaders.DirectListLoader =
    GGRC.ListLoaders.BaseListLoader.extend({}, {
      init: function (modelName, objectAttr, objectJoinAttr) {
        this._super();

        this.model_name = modelName;
        this.object_attr = objectAttr;
        this.object_join_attr = objectJoinAttr;
      },
      init_listeners: function (binding) {
        let self = this;
        let model = directListModels[this.model_name] || Cacheable;

        binding.instance.bind(this.object_join_attr, function (ev, _new, _old) {
          if (binding._refresh_stubs_deferred &&
            binding._refresh_stubs_deferred.state() !== 'pending') {
            self._refresh_stubs(binding);
          }
        });

        model.bind('created', function (ev, mapping) {
          if (mapping instanceof model) {
            self.filter_and_insert_instances_from_mappings(binding, [mapping]);
          }
        });

        model.bind('destroyed', function (ev, mapping) {
          if (mapping instanceof model) {
            self.remove_instance_from_mapping(binding, mapping);
          }
        });

        model.bind('orphaned', function (ev, mapping) {
          if (mapping instanceof model) {
            self.remove_instance_from_mapping(binding, mapping);
          }
        });
      },
      is_valid_mapping: function (binding, mapping) {
        let model = directListModels[this.model_name] || Cacheable;
        let objectModel = binding.instance.constructor;

        return (mapping instanceof model && mapping[this.object_attr] &&
          (reify(mapping[this.object_attr]) === binding.instance ||
          (reify(mapping[this.object_attr]).constructor === objectModel &&
          mapping[this.object_attr].id === binding.instance.id)));
      },
      filter_and_insert_instances_from_mappings: function (binding, mappings) {
        let matchingMappings;

        matchingMappings = _.filteredMap(
          can.makeArray(mappings), (mapping) => {
            if (this.is_valid_mapping(binding, mapping)) {
              return mapping;
            }
          }
        );
        return this.insert_instances_from_mappings(binding, matchingMappings);
      },
      insert_instances_from_mappings: function (binding, mappings) {
        let newResults;

        newResults = _.filteredMap(can.makeArray(mappings),
          (mapping) => this.get_result_from_mapping(binding, mapping));
        this.insert_results(binding, newResults);
      },
      remove_instance_from_mapping: function (binding, mapping) {
        let instance;
        let result;
        if (this.is_valid_mapping(binding, mapping)) {
          instance = this.get_instance_from_mapping(binding, mapping);
          result = this.find_result_from_mapping(binding, mapping);
          if (instance) {
            this.remove_instance(binding, instance, result);
          }
        }
      },
      get_result_from_mapping: function (binding, mapping) {
        return this.make_result({
          instance: mapping,
          mappings: [{
            instance: true,
            mappings: [],
            binding: binding,
          }],
          binding: binding,
        });
      },
      get_instance_from_mapping: function (binding, mapping) {
        return mapping;
      },
      find_result_from_mapping: function (binding, mapping) {
        let result;
        let resultInd;

        for (resultInd = 0; resultInd < binding.list.length; resultInd++) {
          result = binding.list[resultInd];
          if (result.instance === mapping) {
            // DirectListLoader can't have multiple mappings
            return result.mappings[0];
          }
        }
      },
      _refresh_stubs: function (binding) {
        let that = this;
        let refreshQueue = new RefreshQueue();

        refreshQueue.enqueue(binding.instance);

        return refreshQueue.trigger().then(function () {
          let objectJoinAttr = that.object_join_attr;
          let mappings = binding.instance[objectJoinAttr] &&
            reify(binding.instance[objectJoinAttr]);

          that.insert_instances_from_mappings(binding, mappings);
        });
      },
    });
})(window.GGRC, window.can);
