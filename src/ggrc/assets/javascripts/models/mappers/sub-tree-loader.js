/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can) {
  'use strict';

  GGRC.ListLoaders.TreeBaseLoader('GGRC.ListLoaders.SubTreeLoader', {}, {
    load: function (params, models) {
      var snapshots = GGRC.Utils.Snapshots;
      if (snapshots.isSnapshotScope(this.binding.instance) ||
          snapshots.isSnapshotParent(this.binding.instance.type)) {
        params.data = params.data.map(function (item) {
          if (snapshots.isSnapshotModel(item.object_name)) {
            item = snapshots.transformQuery(item);
          }
          return item;
        });
      }
      return GGRC.Utils.QueryAPI.makeRequest(params)
        .then(function (response) {
          var mapped = [];
          models.forEach(function (modelName, idx) {
            var values;
            var models;
            if (snapshots.isSnapshotModel(modelName) &&
                                            response[idx].Snapshot) {
              values = response[idx].Snapshot.values;
            } else {
              values = response[idx][modelName].values;
            }
            values = can.makeArray(values);
            models = values.map(function (source) {
              var result;
              if (source.type === 'Snapshot') {
                result = snapshots.toObject(source);
              } else {
                result = CMS.Models[modelName].model(source);
              }
              return result;
            });
            mapped = mapped.concat(models);
          });
          return mapped;
        })
        .then(function (list) {
          var directlyRelated = [];
          var notRelated = [];
          var result = [];
          var pageUtils = GGRC.Utils.CurrentPage;
          var related = pageUtils.related;
          var needToSplit = pageUtils.isObjectContextPage();

          if (needToSplit) {
            list.forEach(function (inst) {
              var relates = related.attr(inst.type);
              var instId = snapshots.isSnapshot(inst) ?
                inst.snapshot.child_id :
                inst.id;
              if (relates && relates[instId]) {
                directlyRelated.push(inst);
              } else {
                notRelated.push(inst);
              }
            });
            result = directlyRelated.concat(notRelated);
          } else {
            result = list;
          }
          return this.insertInstancesFromMappings(result);
        }.bind(this));
    }
  });
})(GGRC, can);
