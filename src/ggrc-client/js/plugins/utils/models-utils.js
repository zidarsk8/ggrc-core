/*
  Copyright (C) 2018 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

import RefreshQueue from '../../models/refresh_queue';

const relatedAssessmentsTypes = Object.freeze(['Control', 'Objective']);

const getModelInstance = (id, type, requiredAttr) => {
  const promise = new Promise((resolve, reject) => {
    let modelInstance;

    if (!id || !type || !requiredAttr) {
      reject();
    }

    modelInstance = CMS.Models[type].findInCacheById(id) || {};

    if (modelInstance && modelInstance.hasOwnProperty(requiredAttr)) {
      resolve(modelInstance);
    } else {
      modelInstance = new CMS.Models[type]({id: id});
      new RefreshQueue()
        .enqueue(modelInstance)
        .trigger()
        .done((data) => {
          data = Array.isArray(data) ? data[0] : data;
          resolve(data);
        })
        .fail(function () {
          GGRC.Errors
            .notifier('error', `Failed to fetch data for ${type}: ${id}.`);
          reject();
        });
    }
  });

  return promise;
};

/**
 * Check the model has Related Assessments
 * @param {String} type - model type
 * @return {Boolean}
 */
const hasRelatedAssessments = (type) => {
  return _.contains(relatedAssessmentsTypes, type);
};

const resolveDeferredBindings = (obj) => {
  let _pjs;
  let refreshDfds = [];
  let dfds = [];
  let dfdsApply;
  if (obj._pending_joins && obj._pending_joins.length) {
    _pjs = obj._pending_joins.slice(0); // refresh of bindings later will muck up the pending joins on the object
    can.each(can.unique(can.map(_pjs, function (pj) {
      return pj.through;
    })), function (binding) {
      refreshDfds.push(obj.get_binding(binding).refresh_stubs());
    });

    return $.when(...refreshDfds)
      .then(function () {
        can.each(obj._pending_joins, function (pj) {
          let inst;
          let pjDfd;
          let binding = obj.get_binding(pj.through);
          let model = (CMS.Models[binding.loader.model_name] ||
                       GGRC.Models[binding.loader.model_name]);
          if (pj.how === 'add') {
            // Don't re-add -- if the object is already mapped (could be direct or through a proxy)
            // move on to the next one
            if (_.includes(_.map(binding.list, 'instance'), pj.what) ||
               (binding.loader.option_attr &&
                _.includes(_.map(binding.list, function (joinObj) {
                  return joinObj.instance[binding.loader.option_attr];
                }), pj.what))) {
              return;
            }
            inst = pj.what instanceof model
              ? pj.what
              : new model({
                context: obj.context,
              });
            pjDfd = pj.what !== inst && pj.what.isNew()
              ? pj.what.save() : null;
            dfds.push(
              $.when(pjDfd)
                .then(function () {
                  if (binding.loader.object_attr) {
                    inst.attr(binding.loader.object_attr, obj.stub());
                  }
                  if (binding.loader.option_attr) {
                    inst.attr(binding.loader.option_attr, pj.what.stub());
                  }
                  if (pj.extra) {
                    inst.attr(pj.extra);
                  }
                  return inst.save();
                })
            );
          } else if (pj.how === 'update') {
            binding.list.forEach(function (boundObj) {
              let blOptionAttr = binding.loader.option_attr;
              if (boundObj.instance === pj.what ||
                  boundObj.instance[blOptionAttr] === pj.what) {
                boundObj.get_mappings().forEach(function (mapping) {
                  dfds.push(mapping.refresh().then(function () {
                    if (pj.extra) {
                      mapping.attr(pj.extra);
                    }
                    return mapping.save();
                  }));
                });
              }
            });
          } else if (pj.how === 'remove') {
            can.map(binding.list, function (boundObj) {
              let blOptionAttr = binding.loader.option_attr;
              if (boundObj.instance === pj.what ||
                  boundObj.instance[blOptionAttr] === pj.what) {
                can.each(boundObj.get_mappings(), function (mapping) {
                  dfds.push(mapping.refresh().then(function () {
                    mapping.destroy();
                  }));
                });
              }
            });
          }
        });

        dfdsApply = $.when(...dfds);

        obj.attr('_pending_joins', []);
        obj.attr('_pending_joins_dfd', dfdsApply);

        return dfdsApply.then(function () {
          obj.dispatch('resolvePendingBindings');
          return obj.refresh();
        });
      });
  }
  return obj;
};

export {
  getModelInstance,
  hasRelatedAssessments,
  relatedAssessmentsTypes,
  resolveDeferredBindings,
};
