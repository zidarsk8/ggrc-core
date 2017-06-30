/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC, CMS) {
  'use strict';

  var mapper = {
    mapObjects: function (source, destination) {
      return new CMS.Models.Relationship({
        context: source.context || {id: null},
        source: source,
        destination: destination
      });
    }
  };

  GGRC.Components('reusableObjectsList', {
    tag: 'reusable-objects-list',
    viewModel: {
      define: {
        baseInstanceDocuments: {
          get: function () {
            return this.attr('urls').concat(this.attr('evidences'));
          }
        },
        hasSelected: {
          get: function () {
            return this.attr('documentList.length');
          }
        }
      },
      evidences: [],
      urls: [],
      baseInstance: {},
      documentList: [],
      isSaving: false,
      baseInstanceDocuments: [],
      getMapObjects: function (source, list) {
        return list
          .filter(function (item, index) {
            return index === list.indexOf(item);
          })
          // Get Array of mapped models
          .map(function (destination) {
            return mapper
              .mapObjects(source, destination)
              .save();
          });
      },
      reuseSelected: function () {
        var reusedObjectList =
          this.getMapObjects(
            this.attr('baseInstance'),
            this.attr('documentList'));
        this.attr('isSaving', true);

        can.when.apply(can, reusedObjectList)
          .always(this.restoreDefaults.bind(this));
      },
      restoreDefaults: function () {
        this.attr('documentList').replace([]);
        this.attr('isSaving', false);
        this.dispatch('afterObjectReused');
        this.attr('baseInstance').dispatch('refreshInstance');
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
